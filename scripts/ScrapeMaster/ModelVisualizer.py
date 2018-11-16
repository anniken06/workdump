""" Setup:
    $ sudo yum install python libgomp graphviz -y
    $ sudo pip install boto3 mxnet xgboost scikit-learn backports.tempfile
"""

from __future__ import print_function
import sys, traceback, warnings

def my_except_hook(etype, val, tb):
    message = "{}: {}".format(etype.__name__, str(val))
    tb_str = "\t".join(traceback.format_tb(tb))
    print("{}\nTraceback:\n{}".format(message, tb_str), file=sys.stderr)

sys.excepthook = my_except_hook
warnings.filterwarnings('ignore')

import json
import os
import pickle
import re
import tarfile
import tempfile
import uuid
import zipfile

import boto3
import graphviz
import mxnet
import numpy
import scipy
import sklearn, sklearn.ensemble
import xgboost

if sys.version_info.major == 2:
    import backports.tempfile as tempfile
else:
    import tempfile

if sys.maxsize != 2**63 - 1:
    raise Exception("This script must be ran on Python 64-bit.")

gv_major, gv_minor, _ = graphviz.version()
if not (gv_major == 2 and gv_minor >= 38):
    raise Exception("This script must be ran with a separate installation of graphviz version 2.38 or higher.")

s3_model_path, s3_dir_path = sys.argv[1:3]


class NumpyEncoder(json.JSONEncoder):
    """ Special json encoder for numpy types """
    def default(self, obj):
        if isinstance(obj, (numpy.ndarray,)): 
            return obj.tolist()   
        elif isinstance(obj, (mxnet.ndarray.ndarray.NDArray,)): 
            return obj.asnumpy().tolist()
        return json.JSONEncoder.default(self, obj)
    
    @staticmethod
    def jsonify(obj, indent=None):
        return json.dumps(obj, cls=NumpyEncoder, indent=indent)


class FileExtractor:
    @staticmethod  # required decorator for Python 2 methods to become not unbounded
    def unpack_tar_gz_file(file_path, out_dir):
        with tarfile.open(file_path, 'r:gz') as tar_file_handle:
            tar_file_handle.extractall(out_dir)

    @staticmethod
    def unpack_zip_fle(file_path, out_dir):
        with zipfile.ZipFile(file_path) as zip_file_handle:
            zip_file_handle.extractall(out_dir)

    @staticmethod
    def unpack_file(file_path, out_dir):
        if file_path.endswith(".tar.gz"):
            return FileExtractor.unpack_tar_gz_file(file_path, out_dir)
        elif file_path.endswith(".zip"):
            return FileExtractor.unpack_zip_fle(file_path, out_dir)
        else:  # consider files without file extensions
            attempt_unpacks = [FileExtractor.unpack_tar_gz_file, FileExtractor.unpack_zip_fle]
            for unpack in attempt_unpacks:
                try:
                    return unpack(file_path, out_dir)
                except:
                    pass
        raise Exception("Failure in unpacking file.")


class S3Utils:
    client = boto3.resource('s3')
    
    @staticmethod
    def extract_dir_from(s3_path):
        try:
            if s3_path.endswith("/"):
                s3_path = s3_path[ :-1]
            bucket_key_pattern = re.compile("s3://(?P<bucket>.+?)/(?P<key>.+)")
            groups = bucket_key_pattern.match(s3_path).groupdict()
            return (groups['bucket'], groups['key'])
        except:
            raise Exception("Invalid S3 dir path")
    
    @staticmethod
    def parse_s3_model_url(s3_path):
        try:
            model_pattern = re.compile("s3://(?P<bucket>.+?)/" +  # greedy capture until the first slash as bucket
                "(?P<key>.+" +  # group everything after the slash succeeding bucket as key
                    "/artifacts/(?P<model_name>.+)-[0-9]+/output/(?P<file_name>.+)" +  # hard-coded but captures model_name and file_name
                ")")
            return model_pattern.match(s3_path).groupdict()
        except:
            raise Exception("Invalid S3 model path")

    @staticmethod
    def save_file_and_details(s3_path, out_path):
        s3_details = S3Utils.parse_s3_model_url(s3_path)
        s3_details['file_path'] = os.path.join(out_path, s3_details['file_name'])
        S3Utils.client.Bucket(s3_details['bucket']).download_file(s3_details['key'], s3_details['file_path'])
        return s3_details

    @staticmethod
    def upload_dot_model_to_s3(dot_model):
        (upload_bucket, upload_dir) = S3Utils.extract_dir_from(s3_dir_path)
        unique_id = str(uuid.uuid4())
        with tempfile.TemporaryDirectory() as dot_cache_dir:
            dot_cache_path = os.path.join(dot_cache_dir, unique_id)
            with open(dot_cache_path, 'wb') as dot_cache_file:
                dot_cache_file.write(dot_model)
            dot_cache_name = os.path.basename(dot_cache_path)
            S3Utils.client.Bucket(upload_bucket).upload_file(dot_cache_path, "{}/{}".format(upload_dir, dot_cache_name))
        return "s3://{}/{}/{}".format(upload_bucket, upload_dir, dot_cache_name)


class ModelVisualizer:
    @staticmethod
    def find_model_file_in(model_dir, model_file_keyword=""):
        files = os.listdir(model_dir)
        file = next(file for file in reversed(files) if model_file_keyword in file)  # sort the file names by descending order and pick the first one
        return os.path.join(model_dir, file)

    @staticmethod
    def load_pkl_model(model_path, encoding='latin1', **kwargs):
        """ Reference: http://scikit-learn.org/stable/modules/model_persistence.html#security-maintainability-limitations, https://stackoverflow.com/questions/21033038/scikits-learn-randomforrest-trained-on-64bit-python-wont-open-on-32bit-python
            Note: This must be must be ran under the same architecture (64-bit) where the model was picked. """
        with open(model_path, 'rb') as model_pickle:
            if sys.version_info.major == 2:
                return pickle.load(model_pickle, **kwargs)
            return pickle.load(model_pickle, encoding=encoding, **kwargs)

    @staticmethod
    def load_mxnet_ndarray(model_path):
        return mxnet.ndarray.load(model_path)

    @staticmethod
    def load_mxnet_archive(model_path, prefix, epoch, **kwargs):
        model_dir = os.path.dirname(model_path)
        FileExtractor.unpack_file(model_path, model_dir)
        path_prefix = os.path.join(model_dir, prefix)
        return mxnet.module.Module.load(path_prefix, epoch, **kwargs)
    
    @staticmethod
    def format_dot_model(dot_model):
        dot_model = re.sub("shape=[a-z]+", "shape=box", dot_model)
        # other formatting
        return dot_model

    @staticmethod
    def visualize_dot_model(dot_model, do_upload=False):
        """ Handles the representation of dot models """
        dot_model = ModelVisualizer.format_dot_model(dot_model)
        if do_upload:
            return S3Utils.upload_dot_model_to_s3(dot_model.encode('utf-8'))
        else:
            return dot_model

    @staticmethod
    def visualize_tree_model(model):
        """ Reference: http://scikit-learn.org/stable/modules/generated/sklearn.tree.export_graphviz.html  """
        try:
            dot_str = sklearn.tree.export_graphviz(model, out_file=None, class_names=True, node_ids=True)
            tree = ModelVisualizer.visualize_dot_model(dot_str)
        except:
            tree = None
        return {"parameters": model.get_params(), "tree": tree}

    @staticmethod
    def get_details_xgboost_model(model_path):
        """ Reference: https://xgboost.readthedocs.io/en/latest/python/python_api.html#xgboost.to_graphviz, https://xgboost.readthedocs.io/en/latest/python/python_api.html#xgboost.train """
        model = ModelVisualizer.load_pkl_model(model_path)
        booster_dots = []
        for i in range(model.best_ntree_limit):
            dot_model = xgboost.to_graphviz(model, num_trees=i, yes_color='#000000', no_color='#000000')
            booster_dots += [ModelVisualizer.visualize_dot_model(dot_model.source)]
        return {"boosters": booster_dots[ :5]}  ### TEMP [ :5]

    @staticmethod
    def get_details_linear_learner_model(model_path):
        """ Reference: https://forums.aws.amazon.com/thread.jspa?messageID=827236#827236 
            Note: symbol_dot = mxnet.viz.plot_network(model.symbol).source  # "computationalGraph": symbol_dot """
        model_dir = os.path.dirname(model_path)
        FileExtractor.unpack_file(model_path, model_dir)
        params_file_path = ModelVisualizer.find_model_file_in(model_dir, model_file_keyword=".params")
        params_file_name = os.path.basename(params_file_path)
        params_file_name_pattern = re.compile("(?P<prefix>.+)-(?P<epoch>[0-9]+)\.params")
        params_details = params_file_name_pattern.match(params_file_name).groupdict()
        (prefix, epoch) = (params_details['prefix'], int(params_details['epoch']))
        model = ModelVisualizer.load_mxnet_archive(model_path, prefix, epoch)
        weight_matrix = model._arg_params['fc0_weight']
        bias_matrix = model._arg_params['fc0_bias']
        return {"weightMatrix": weight_matrix, "biasMatrix": bias_matrix}

    @staticmethod
    def get_details_k_means_model(model_path):
        """ Reference: https://github.com/awslabs/amazon-sagemaker-examples/blob/master/introduction_to_applying_machine_learning/US-census_population_segmentation_PCA_Kmeans/sagemaker-countycensusclustering.ipynb """
        model = ModelVisualizer.load_mxnet_ndarray(model_path)
        centroids = model[0]
        return {"centroids": centroids}

    @staticmethod
    def get_details_sklearn_tree_model(model_path):
        model = ModelVisualizer.load_pkl_model(model_path)
        return ModelVisualizer.visualize_tree_model(model)

    @staticmethod
    def get_details_sklearn_forest_model(model_path):
        model = ModelVisualizer.load_pkl_model(model_path)
        base_estimator_dot = ModelVisualizer.visualize_tree_model(model.base_estimator)
        estimators_dot = [ModelVisualizer.visualize_tree_model(estimator) for estimator in model.estimators_]
        return {"parameters": model.get_params(), "baseEstimator": base_estimator_dot, "estimators": estimators_dot[ :5]}  ### TEMP [ :5]

    @staticmethod
    def get_details_principle_component_analysis_model(model_path):
        """ Reference: https://github.com/awslabs/amazon-sagemaker-examples/blob/master/introduction_to_applying_machine_learning/US-census_population_segmentation_PCA_Kmeans/sagemaker-countycensusclustering.ipynb """
        model = ModelVisualizer.load_mxnet_ndarray(model_path)
        mean = model.get('mean', None)
        principle_components = model['v']
        transformation_singular_values = model['s']
        return {"mean": mean, "principleComponents": principle_components, "transformationSingularValues": transformation_singular_values}

    @staticmethod
    def get_details_generic_model(model_name, model_path):
        model_details = {
            'xgboost': ModelVisualizer.get_details_xgboost_model,
            'linear-learner': ModelVisualizer.get_details_linear_learner_model,
            'k-means': ModelVisualizer.get_details_k_means_model,
            'decision-tree-classification': ModelVisualizer.get_details_sklearn_tree_model,
            'random-forest-classification': ModelVisualizer.get_details_sklearn_forest_model,
            'extra-trees-classification': ModelVisualizer.get_details_sklearn_forest_model,
            'principal-component-analysis': ModelVisualizer.get_details_principle_component_analysis_model,
            # TODO: add more
        }[model_name](model_path)
        return NumpyEncoder.jsonify(model_details, indent=4)

    @staticmethod
    def retrieve_model_properties_from_s3(s3_path):
        with tempfile.TemporaryDirectory() as temp_download_dir,\
                tempfile.TemporaryDirectory(dir=temp_download_dir) as temp_unpack_dir:
            file_details = S3Utils.save_file_and_details(s3_path, temp_download_dir)
            FileExtractor.unpack_file(file_details['file_path'], temp_unpack_dir)
            model_path = ModelVisualizer.find_model_file_in(temp_unpack_dir, model_file_keyword="model")
            return ModelVisualizer.get_details_generic_model(file_details['model_name'], model_path)


if __name__ == '__main__':  # dump the results into stdout
    print(ModelVisualizer.retrieve_model_properties_from_s3(s3_model_path), file=sys.stdout)
