import boto3
import io
import json
import pickle
import tarfile
import zipfile

from urlparse import urlparse


""" problem with some file handles not having seek() + some unpicklers not accepting raw bytes
from sklearn.externals import joblib
def attempts_to_unpickle(file_handle):
    unpickling_methods = [pickle.load, joblib.load]
    file_data = file_handle.read()
    for unpickling_method in unpickling_methods:
        try:
            return unpickling_method(file_handle)
        except Exception as e:
            print("Failed to unpickle {file_handle} using {unpickling_method}:\n\t{e}".format(**locals()))
    raise Exception("Could not to unpickle {file_handle} using any unpickling method".format(**locals()))
"""

def is_model_file(file_path, model_keyword="model"):
    return model_keyword in file_path

def get_s3_file_stream(s3_path):
    parsed_url = urlparse(s3_path)
    (bucket, key) = (parsed_url.netloc, parsed_url.path[1: ])
    client = boto3.resource('s3')
    obj = client.Object(bucket_name=bucket, key=key)
    return io.BytesIO(obj.get()['Body'].read())

from contextlib import closing  # required by older TarFile.extractfile with-context
def load_targz_model(tar_gz_byte_buffer):
    with tarfile.open('r:gz', fileobj=tar_gz_byte_buffer) as tar_file_handle:
        model_file = next(file for file in tar_file_handle.getmembers() if is_model_file(file.path))
        with closing(tar_file_handle.extractfile(model_file)) as model_file_handle:
            return pickle.load(model_file_handle)

def load_zip_model(zip_file_byte_buffer):
    with zipfile.ZipFile(zip_file_byte_buffer) as zip_file_handle:
        model_file = next(file for file in zip_file_handle.namelist() if is_model_file(file))
        with zip_file_handle.open(model_file) as model_file_handle:
            return pickle.load(model_file_handle) 

def load_model(s3_path, **kwargs):
    file_buffer = get_s3_file_stream(s3_path)
    if s3_path.endswith(".tar.gz"):
        return load_targz_model(file_buffer)
    elif s3_path.endswith(".zip"):
        return load_zip_model(file_buffer)
    else:
        raise Exception('Model archive type for "{s3_path}" is not supported.'.format(**locals()))

def jsonify_model(model):  # this is hacky
    print("Serializing {model}...".format(**locals()))
    attrs = {}
    for (k, v) in model.__dict__.items():
        try:
            json.dumps(v)
            attrs[k] = v
        except Exception as e:
            print('Failed to serialize "{k}": {e}. Casting as string...'.format(**locals()))
            attrs[k] = str(v)
    return json.dumps(attrs, indent=4)


if __name__ == '__main__':
    model_s3_paths = [
        "s3://infor-analytics-team/coleman/INTEGRATION_AX1/conversions/d386c9ab-4152-419a-9720-f9b1782a8ae8/artifacts/xgboost-1537163579581/output/model.tar.gz",
        "s3://coleman-manila-team/xgboost-model.zip",
        "s3://infor-analytics-team/coleman/INTEGRATION_AX1/conversions/8b83a72d-234a-44d8-ba99-ddd35a932377/artifacts/random-forest-classification-1537163579721/output/model.tar.gz",  # depickling error
        "s3://infor-analytics-team/coleman/IntegrationTests/INTEGRATION_AX1/datasets/input/externalData/2db98f65-6fdf-4522-9c64-07c4fdedf39d/artifacts/linear-learner-1537166858565/output/model.tar.gz",  # depickling error
    ]
    model_dict = {path: load_model(path) for path in model_s3_paths}
    model_dict_jsons = {path: jsonify_model(model) for (path, model) in model_dict.items()}
    for (path, json) in model_dict_jsons.items():
        print("Printing json for model: {path}:".format(**locals()))
        print(json)

    import code; code.interact(local=locals())
