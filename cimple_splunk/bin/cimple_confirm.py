from splunk.persistconn.application import PersistentServerConnectionApplication
import json

PROPS_CONF="/opt/splunk/etc/apps/applog/local/props.conf"

TAGS_CONF="/opt/splunk/etc/apps/applog/local/tags.conf"

def save_to_file(filename, content):
    with open(filename, 'a') as file:
        file.write(content)

class CimpleConfirm(PersistentServerConnectionApplication):
    def __init__(self, _command_line, _command_arg):
        super(PersistentServerConnectionApplication, self).__init__()

    # Handle a syncronous from splunkd.
    def handle(self, in_string):
        decoded_string = in_string.decode('utf-8')

        # Parsing the JSON data
        data = json.loads(decoded_string)

        form_data = ""
        return_msg = "Confirmed"
        if 'form' in data:
            form_data = data['form']
            confirm_data = json.loads(form_data[0][0])

            data_model = []

            for x in confirm_data:
                try:
                    # save_to_file(TAGS_CONF, f"{x['data-model']} = enabled\n")
                    data_model.append(x['data-model'])

                    save_to_file(PROPS_CONF, f"FIELDALIAS-{x['data-model']}-{x['input']} = {x['input']} as {x['field']}\n")
                except Exception:
                    return {'payload': "Failed", 'status': 500}
                
            unique_values = set(data_model)
            for u in unique_values:
                save_to_file(TAGS_CONF, f"{u} = enabled\n")


        return {'payload': "Confirmed", 'status': 200}

    def handleStream(self, handle, in_string):
        raise NotImplementedError(
            "PersistentServerConnectionApplication.handleStream")

    def done(self):
        pass

