import flask
import kubernetes


APP = flask.Flask(__name__)
K8S_URL = 'https://kubernetes.default.svc.cluster.local'
API_GROUP = 'khmarochos.melnyk.host'
API_VERSION = 'v1'
KIND_PLURAL = 'dummyobjects'
with open('/var/run/secrets/kubernetes.io/serviceaccount/namespace', 'r') as f:
    NAMESPACE = f.read().strip()


@APP.route("/<string:dummy_object_name>", methods=["GET"])
def get_dummy_object(dummy_object_name):
    try:
        api_instance = kubernetes.client.CustomObjectsApi()
        obj = api_instance.get_namespaced_custom_object(
            group=API_GROUP,
            version=API_VERSION,
            namespace=NAMESPACE,
            plural=KIND_PLURAL,
            name=dummy_object_name
        )
        return flask.jsonify({'dummy_message': obj.get('spec').get('message')}), 200
    except Exception as e:
        return flask.jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    kubernetes.config.load_incluster_config()
    kubernetes.client.Configuration().host = K8S_URL
    APP.run(debug=False, host='0.0.0.0')