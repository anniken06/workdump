#!/usr/bin/python3
import warnings; warnings.filterwarnings("ignore", category=DeprecationWarning)

import boto3
import io
import json
import mxnet
import os
import pickle
import regex
import tarfile
import tempfile
import zipfile

from sklearn.externals import joblib


def parse_s3_url(s3_path):
    s3_pattern = regex.compile(
        "s3://(?P<bucket>.+?)/" +  # greedy capture until the first slash as bucket
        "(?P<key>.+" +  # group everything after the slash succeeding bucket as key
            "/artifacts/(?P<model_name>.+)-[0-9]+/output/(?P<file_name>.+)" +  # hard-coded but captures model_name and file_name
        ")")
    return s3_pattern.match(s3_path).groupdict()

def download_s3_file(s3_path, out_path):
    s3_details = parse_s3_url(s3_path)
    s3_details['file_path'] = os.path.join(out_path, s3_details['file_name'])
    client = boto3.resource('s3')
    client.Bucket(s3_details['bucket']).download_file(s3_details['key'], s3_details['file_path'])
    return s3_details

def unpack_generic_file(file_path, out_dir):
    if file_path.endswith(".tar.gz"):
        return unpack_tar_gz_file(file_path, out_dir)
    elif file_path.endswith(".zip"):
        return unpack_zip_fle(file_path, out_dir)
    else:  # consider files without file extensions
        attempt_unpacks = [unpack_tar_gz_file, unpack_zip_fle]
        for unpack in attempt_unpacks:
            try: return unpack(file_path, out_dir)
            except: pass
    raise Exception(f'Model archive type for the file "{file_path}" is not supported.')

def unpack_tar_gz_file(file_path, out_dir):
    with tarfile.open(file_path, 'r:gz') as tar_file_handle:
        tar_file_handle.extractall(out_dir)

def unpack_zip_fle(file_path, out_dir):
    with zipfile.ZipFile(file_path) as zip_file_handle:
        zip_file_handle.extractall(out_dir)

def find_model_file_in(model_dir, model_file_keyword="model"):
    files = os.listdir(model_dir)
    file = next(file for file in files if model_file_keyword in file)  # take the first file that satisfies the condition
    return os.path.join(model_dir, file)

def load_xgboost_model(model_path, **kwargs):
    """Reference: "Anany, Moataz" <moanany@amazon.com>"""
    with open(model_path, 'rb') as model_pickle:
        return pickle.load(model_pickle, **kwargs)

def load_linear_learner_model(model_path, prefix="mx-mod", epoch=0, **kwargs):
    """Reference: https://forums.aws.amazon.com/thread.jspa?messageID=827236#827236"""
    model_dir = os.path.dirname(model_path)
    unpack_generic_file(model_path, model_dir)
    return mxnet.module.Module.load(os.path.join(model_dir, prefix), epoch, **kwargs)

def load_random_forest_classification_model(model_path, **kwargs):
    # return pickle.load(open(model_path, 'rb'), encoding='latin1')
    ##   File "sklearn\tree\_tree.pyx", line 601, in sklearn.tree._tree.Tree.__cinit__ ValueError: Buffer dtype mismatch, expected 'SIZE_t' but got 'long long'
    return joblib.load(model_path, **kwargs)

def load_kmeans_model(model_path):
    """Reference: "Anany, Moataz" <moanany@amazon.com>"""
    pass
    """ KMeans Notes:
    The k-means model artifact is an MXNet NDArray.  So, they can access the model artifact with:
    $ aws s3 cp s3://path/to/model/artifact/model.tar.gz ./ && tar xzvf model.tar.gz
    import mxnet as mx
    centroids = mx.ndarray.load('model_algo-1')[0].asnumpy()
    The artifact will be an k * feature_dim array for the k cluster centroids. 
    """

def load_generic_model(model_path, model_name, **kwargs):
    return {
        'xgboost': load_xgboost_model,
        'linear-learner': load_linear_learner_model,
        'random-forest-classification': load_random_forest_classification_model,
    }[model_name](model_path, **kwargs)

def generate_model(s3_path, base_dir=None):
    with tempfile.TemporaryDirectory(dir=base_dir) as temp_download_dir:
        file_details = download_s3_file(s3_path, temp_download_dir)
        with tempfile.TemporaryDirectory(dir=temp_download_dir) as temp_unpack_dir:
            unpack_generic_file(file_details['file_path'], temp_unpack_dir)
            model_path = find_model_file_in(temp_unpack_dir)
            return load_generic_model(model_path, file_details['model_name'])

def jsonify_model(model):  # temporary hacky code for visualizing model
    print(f"Serializing {model}...")
    attrs = {}
    for (k, v) in model.__dict__.items():
        try:
            json.dumps(v)
            attrs[k] = v
        except Exception as e:
            print(f'Failed to json serialize "{k}": {e}.')
    return json.dumps(attrs, indent=4)


if __name__ == '__main__':
    model_s3_paths = [
        "s3://infor-analytics-team/coleman/INTEGRATION_AX1/conversions/d386c9ab-4152-419a-9720-f9b1782a8ae8/artifacts/xgboost-1537163579581/output/xgboost-model.zip",
        "s3://infor-analytics-team/coleman/INTEGRATION_AX1/conversions/d386c9ab-4152-419a-9720-f9b1782a8ae8/artifacts/xgboost-1537163579581/output/model.tar.gz",
        "s3://infor-analytics-team/coleman-ps/INTEGRATION_AX1/conversions/dadc138b-aab7-449a-9b24-7eccb9c80303/artifacts/linear-learner-1537193547948/output/model.tar.gz",
        "s3://infor-analytics-team/coleman/INTEGRATION_AX1/conversions/8b83a72d-234a-44d8-ba99-ddd35a932377/artifacts/random-forest-classification-1537163579721/output/model.tar.gz",
        #"s3://infor-analytics-team/coleman/IntegrationTests/INTEGRATION_AX1/datasets/input/externalData/0db98f65-6fdf-4522-9c64-07c4fdedf39a/artifacts/extra-trees-classification-1537157999586/output/model.tar.gz",
    ]
    model_dict = {path: generate_model(path, base_dir="C:/Users/jguzman2/OneDrive - Infor/Desktop/pytask") for path in model_s3_paths}
    for (path, model) in model_dict.items():
        print(f"Printing json for model: {path}:")
        print(jsonify_model(model))

    import code; code.interact(local={**locals(), **globals()})

""" Notes:
Here are some examples of what we need to extract from the model
-   coefficients (linear regression), 
-   coordinates of cluster centers (kmeans), 
-   splits (decision trees), 
-   feature importance, 
and probably some other statistics
"""
