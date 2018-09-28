import json
import os
import pickle
import re
import sys
import tarfile
import tempfile
import zipfile

# requirements: # pip install boto3 mxnet scikit-learn scipy xgboost
import boto3
import mxnet
import numpy
import sklearn

import xgboost, scipy  # unused imports, but required for depickling
if not (sys.version_info.major == 3 and sys.maxsize == 2**63 - 1):
    raise Exception("This script must be ran on Python 3 64-bit.")


class FileExtractor:
    def unpack_tar_gz_file(file_path, out_dir):
        with tarfile.open(file_path, 'r:gz') as tar_file_handle:
            tar_file_handle.extractall(out_dir)

    def unpack_zip_fle(file_path, out_dir):
        with zipfile.ZipFile(file_path) as zip_file_handle:
            zip_file_handle.extractall(out_dir)

    def unpack_file(file_path, out_dir):
        if file_path.endswith(".tar.gz"):
            return FileExtractor.unpack_tar_gz_file(file_path, out_dir)
        elif file_path.endswith(".zip"):
            return FileExtractor.unpack_zip_fle(file_path, out_dir)
        else:  # consider files without file extensions
            attempt_unpacks = [FileExtractor.unpack_tar_gz_file, FileExtractor.unpack_zip_fle]
            for unpack in attempt_unpacks:
                try: return unpack(file_path, out_dir)
                except: pass
        raise Exception("Failure in unpacking file.")


class S3Utils:
    def parse_s3_url(s3_path):
        s3_pattern = re.compile(
            "s3://(?P<bucket>.+?)/" +  # greedy capture until the first slash as bucket
            "(?P<key>.+" +  # group everything after the slash succeeding bucket as key
                "/artifacts/(?P<model_name>.+)-[0-9]+/output/(?P<file_name>.+)" +  # hard-coded but captures model_name and file_name
            ")")
        return s3_pattern.match(s3_path).groupdict()

    def save_file_and_details(s3_path, out_path):
        s3_details = S3Utils.parse_s3_url(s3_path)
        s3_details['file_path'] = os.path.join(out_path, s3_details['file_name'])
        client = boto3.resource('s3')
        client.Bucket(s3_details['bucket']).download_file(s3_details['key'], s3_details['file_path'])
        return s3_details


class NumpyEncoder(json.JSONEncoder):
    """ Special json encoder for numpy types """
    def default(self, obj):
        if isinstance(obj, (numpy.ndarray,)): 
            return obj.tolist()   
        elif isinstance(obj, (mxnet.ndarray.ndarray.NDArray,)): 
            return obj.asnumpy().tolist()
        return json.JSONEncoder.default(self, obj)

    def jsonify(obj, indent=None):
        return json.dumps(obj, cls=NumpyEncoder, indent=indent)


class ModelVisualizer:
    def find_model_file_in(model_dir, model_file_keyword=""):
        files = os.listdir(model_dir)
        file = next(file for file in reversed(files) if model_file_keyword in file)  # sort the file names by descending order and pick the first one
        return os.path.join(model_dir, file)

    def load_pkl_model(model_path, encoding='latin1', **kwargs):
        """ Reference: http://scikit-learn.org/stable/modules/model_persistence.html#security-maintainability-limitations, https://stackoverflow.com/questions/21033038/scikits-learn-randomforrest-trained-on-64bit-python-wont-open-on-32bit-python
        Note: This must be must be ran under the same architecture (64-bit) where the model was picked. """
        with open(model_path, 'rb') as model_pickle:
            return pickle.load(model_pickle, encoding=encoding, **kwargs)

    def load_mxnet_model(model_path, prefix, epoch, **kwargs):
        """ Reference: https://forums.aws.amazon.com/thread.jspa?messageID=827236#827236 """
        model_dir = os.path.dirname(model_path)
        FileExtractor.unpack_file(model_path, model_dir)
        path_prefix = os.path.join(model_dir, prefix)
        return mxnet.module.Module.load(path_prefix, epoch, **kwargs)

    def get_details_xgboost_model(model_path):
        model = ModelVisualizer.load_pkl_model(model_path)
        return {"modelData": [json.loads(j) for j in model.get_dump(with_stats=True, dump_format='json')]}

    def get_details_mxnet_model(model_path):
        model_dir = os.path.dirname(model_path)
        FileExtractor.unpack_file(model_path, model_dir)
        params_file_path = ModelVisualizer.find_model_file_in(model_dir, model_file_keyword=".params")
        params_file_name = os.path.basename(params_file_path)
        params_file_name_pattern = re.compile("(?P<prefix>.+)-(?P<epoch>[0-9]+)\.params")
        params_details = params_file_name_pattern.match(params_file_name).groupdict()
        (prefix, epoch) = (params_details['prefix'], int(params_details['epoch']))
        model = ModelVisualizer.load_mxnet_model(model_path, prefix, epoch)
        return {"parameters": model._arg_params}

    def parse_sklearn_tree(model):
        """ Reference: http://scikit-learn.org/stable/modules/generated/sklearn.tree.export_graphviz.html """
        try:
            """
            TODO:
                -convert dot to json
                --requires separate installation of graphviz (<apt-get/brew/choco> install graphviz),
                --and added included in $PATH
            PROBLEM: 
                -json output is only available on graphviz 2.4
                --some systems may not have this update; e.g., latest version on windows == 2.38
            
            import graphviz
            data_dot = sklearn.tree.export_graphviz(model, out_file=None, class_names=True, node_ids=True)
            data_json = graphviz.pipe(engine='dot', format='json', data=data_dot)
            return data_json
            """
            data_dot = sklearn.tree.export_graphviz(model, out_file=None, class_names=True, node_ids=True)
            return data_dot
        except:
            return None

    def get_details_sklearn_tree_model(model_path):
        model = ModelVisualizer.load_pkl_model(model_path)
        if isinstance(model, sklearn.ensemble.forest.BaseForest):
            model_data = {
                "baseEstimator": ModelVisualizer.parse_sklearn_tree(model.base_estimator),
                "estimators": [ModelVisualizer.parse_sklearn_tree(estimator) for estimator in model.estimators_],
            }
        else:
            model_data = {"tree": ModelVisualizer.parse_sklearn_tree(model)}
        return {"hyperparameters": model.get_params(), "modelData": model_data}

    def get_details_k_means_model(model_path):
        """ Reference: "Anany, Moataz" <moanany@amazon.com>
        Note: The k-means model artifact is an MXNet NDArray. So, they can access the model artifact with: centroids = mx.ndarray.load('model_algo-1')[0].asnumpy()
        The artifact will be an k * feature_dim array for the k cluster centroids. """
        return {"centroids": mxnet.ndarray.load(model_path)[0]}

    def get_details_generic_model(model_name, model_path):
        model_details = {
            'xgboost': ModelVisualizer.get_details_xgboost_model,
            'linear-learner': ModelVisualizer.get_details_mxnet_model,
            'random-forest-classification': ModelVisualizer.get_details_sklearn_tree_model,
            'extra-trees-classification': ModelVisualizer.get_details_sklearn_tree_model,
            'decision-tree-classification': ModelVisualizer.get_details_sklearn_tree_model,
            'k-means': ModelVisualizer.get_details_k_means_model,
            # TODO: add more
        }[model_name](model_path)
        return NumpyEncoder.jsonify(model_details, indent=4)

    def retrieve_model_properties_from_s3(s3_path):
        with tempfile.TemporaryDirectory() as temp_download_dir,\
                tempfile.TemporaryDirectory(dir=temp_download_dir) as temp_unpack_dir:
            file_details = S3Utils.save_file_and_details(s3_path, temp_download_dir)
            FileExtractor.unpack_file(file_details['file_path'], temp_unpack_dir)
            model_path = ModelVisualizer.find_model_file_in(temp_unpack_dir, model_file_keyword="model")
            return ModelVisualizer.get_details_generic_model(file_details['model_name'], model_path)

    def __call__(self, **inputs):
        return ModelVisualizer.retrieve_model_properties_from_s3(inputs['s3URL'])


if __name__ == '__main__':  # Test script
    model_s3_paths = [
        "s3://infor-analytics-team/coleman/INTEGRATION_AX1/conversions/d386c9ab-4152-419a-9720-f9b1782a8ae8/artifacts/xgboost-1537163579581/output/model.tar.gz",
        "s3://infor-analytics-team/coleman-ps/INTEGRATION_AX1/conversions/dadc138b-aab7-449a-9b24-7eccb9c80303/artifacts/linear-learner-1537193547948/output/model.tar.gz",
        "s3://infor-analytics-team/coleman/INTEGRATION_AX1/conversions/8b83a72d-234a-44d8-ba99-ddd35a932377/artifacts/random-forest-classification-1537163579721/output/model.tar.gz",
        "s3://infor-analytics-team/coleman/IntegrationTests/INTEGRATION_AX1/datasets/input/externalData/0db98f65-6fdf-4522-9c64-07c4fdedf39a/artifacts/extra-trees-classification-1537157999586/output/model.tar.gz",
        "s3://infor-analytics-team/coleman/IntegrationTests/INTEGRATION_AX1/datasets/input/externalData/3db98f65-6fdf-4522-9c64-07c4fdedf39e/artifacts/decision-tree-classification-1537329311821/output/model.tar.gz",
        "s3://infor-analytics-team/coleman/IntegrationTests/INTEGRATION_AX1/datasets/input/externalData/0db98f65-6fdf-4522-9c64-07c4fdedf39a/artifacts/k-means-1537337029771/output/model.tar.gz",
        # TODO: add more
    ]
    for s3_path in model_s3_paths:
        jsoned = ModelVisualizer()(s3URL=s3_path)
        save_name = s3_path[s3_path.index("/artifacts/") + len("/artifacts/"): s3_path.index("/output/")]
        save_path = ".\\models\\{}.json".format(save_name)
        json.dump(json.loads(jsoned), open(save_path, 'w'), cls=NumpyEncoder, indent=4)
        print("Saved {save_name} to {save_path}".format(**locals()))
