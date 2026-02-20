import json
import os
import argparse
import copy
from os.path import exists

def check_entity(entity):
    if 'title' not in entity.keys():
        pass

def merge_entities(json_root, import_name):
    if isinstance(import_name, dict):
        json_node = import_name
    else:
        with open(import_name) as f1:
            json_node = json.load(f1)

    merge_list = []
    json_node["entities"] = json_node.get("entities", [])
    json_root["entities"] = json_root.get("entities", [])
    for e_node in json_node['entities']:
        check_entity(e_node)

        for e_root in json_root['entities']:
            if e_root['name'] == e_node['name'] and not 'model' in e_root.keys() and not 'model' in e_node.keys():
                root_vals = e_root['values']
                root_vals.extend(e_node['values'])
                root_vals = set(root_vals)
                e_root['values'] = list(root_vals)
                merge_list.append(e_node['name'])

        if e_node['name'] not in merge_list:
            json_root['entities'].append(e_node)

    return json_root

def check_customer_state(customer_state):
    if 'name' not in customer_state.keys():
        pass
def merge_customer_states(json_root, import_name):
    if isinstance(import_name, dict):
        json_node = import_name
    else:
        with open(import_name) as f1:
            json_node = json.load(f1)


    json_node["customer_states"] = json_node.get("customer_states", [])
    json_root["customer_states"] = json_root.get("customer_states", [])
    for cs_node in json_node['customer_states']:
        check_customer_state(cs_node)

        merge_list = []
        for cs_root in json_root['customer_states']:
            if cs_root['name'] == cs_node['name']:

                if "merge_follow_up" in cs_root.keys() and cs_root["merge_follow_up"]:
                    merged_follow_up = cs_node['follow_up'].copy()
                    merged_follow_up.update(cs_root['follow_up'])
                else:
                    merged_follow_up = cs_root['follow_up']
                cs_root['follow_up'] = merged_follow_up
                if ('faq' not in cs_root.keys() or cs_root['faq'] == '') and 'faq' in cs_node.keys():
                    cs_root['faq'] = cs_node['faq']
                if not cs_root.get("override_to_response_function", False) and ('to_response_function' not in cs_root.keys() or len(cs_root['to_response_function'].keys()) == 0) and 'to_response_function' in cs_node.keys():
                    cs_root['to_response_function'] = cs_node['to_response_function']

                if 'required_state' in cs_node.keys():
                    cs_root['required_state'] = cs_node['required_state']
                if 'ui_element' in cs_node.keys():
                    cs_root['ui_element'] = cs_node['ui_element']
                root_keywords = cs_root['keywords']
                if not cs_root.get("override_keywords", False):
                    root_keywords.extend(cs_node['keywords'])
                root_keywords = set(root_keywords)
                cs_root['keywords'] = list(root_keywords)
                merge_list.append(cs_node['name'])

        if cs_node['name'] not in merge_list:
            json_root['customer_states'].append(cs_node)

    return json_root

def check_system_response(system_response):
    if 'name' not in system_response.keys():
        pass
def merge_system_responses(json_root, import_name):
    if isinstance(import_name, dict):
        json_node = import_name
    else:
        with open(import_name) as f1:
            json_node = json.load(f1)


    merge_list = []

    json_node["system_responses"] = json_node.get("system_responses", [])
    json_root["system_responses"] = json_root.get("system_responses", [])
    for sr_node in json_node['system_responses']:
        check_system_response(sr_node)

        for sr_root in json_root['system_responses']:
            if sr_root['name'] == sr_node['name']:
                placeholder_dict = {}
                # Add root placeholders
                if isinstance(sr_root['placeholder'], dict):
                    placeholder_dict.update(sr_root['placeholder'])
                else:
                    placeholder_dict[sr_root['placeholder']] = 1
                sr_root['placeholder'] = placeholder_dict
                root_state_options = sr_root['state_options']
                root_state_options.extend(sr_node['state_options'])
                root_state_options = set(root_state_options)
                sr_root['state_options'] = list(root_state_options)
                if 'data' in sr_root.keys() and 'data' in sr_node.keys() and type(sr_node["data"])==dict and type(sr_root["data"])==dict:
                    if ('_follow_ups' in sr_root['data'].keys() and '_follow_ups' in sr_node['data'].keys()):
                        sr_root['data']['_follow_ups'].extend(sr_node['data']['_follow_ups'])
                    if ('data' not in sr_root.keys() or len(sr_root['data'].keys()) == 0) and 'data' in sr_node.keys():
                        sr_root['data'] = sr_node['data']
                if ('whiteboard' not in sr_root.keys() or sr_root['whiteboard'] == '') and 'whiteboard' in sr_node.keys():
                    sr_root['whiteboard'] = sr_node['whiteboard']
                    sr_root['whiteboard_template'] = sr_node['whiteboard_template']
                    if isinstance(sr_root['data'], dict):
                        temp = sr_root['data'].copy()
                        sr_root['data'].update(sr_node['data'])
                        sr_root['data'].update(temp)
                    else:
                        temp = sr_root['data']
                        sr_root['data'] = temp
                if ('wait' not in sr_root.keys() or sr_root['wait'] == '') and 'wait' in sr_node.keys():
                    sr_root['wait'] = sr_node['wait']
                if 'to_state_function' in sr_node.keys():
                    sr_root['to_state_function'] = sr_node['to_state_function']
                merge_list.append(sr_node['name'])

        if sr_node['name'] not in merge_list:
            json_root['system_responses'].append(sr_node)

    return json_root

def merge_speech_phrases(json_root, import_name):
    speech_phrases_merged = {}

    json_root["speech_phrases"] = json_root.get("speech_phrases", {})

    if json_root['speech_phrases']:
        speech_phrases_merged.update(json_root['speech_phrases'])

    json_node = {}
    if isinstance(import_name, dict):
        json_node = import_name
    else:
        with open(import_name) as f1:
            json_node = json.load(f1)


    merge_list = []
    json_node["speech_phrases"] = json_node.get("speech_phrases", {})

    if 'speech_phrases' in json_node.keys():
        for sp_node_lang in json_node['speech_phrases'].keys():
            if sp_node_lang not in json_root['speech_phrases'].keys():
                speech_phrases_merged[sp_node_lang] = json_node['speech_phrases'][sp_node_lang]
            else:
                speech_phrases_merged[sp_node_lang].extend(json_node['speech_phrases'][sp_node_lang])
                speech_phrases_merged[sp_node_lang] = list(set(speech_phrases_merged[sp_node_lang]))

    json_root['speech_phrases'] = speech_phrases_merged

    return json_root

def merge_translations(json_root, import_name):

    translations_merged = {}

    json_root["translations"] = json_root.get("translations", {})
    json_node = {}

    if isinstance(import_name, dict):
        json_node = import_name
    else:
        with open(import_name) as f1:
            json_node = json.load(f1)


    json_node["translations"] = json_node.get("translations", {})

    translations_merged = copy.deepcopy(json_node['translations'])

    translations_merged.update(json_root['translations'])

    json_root['translations'] = translations_merged

    return json_root

def merge_data(json_root, import_name):

    data_merged = {}

    json_root["data"] = json_root.get("data", {})

    if json_root['data']:
        data_merged.update(json_root['data'])

    if isinstance(import_name, dict):
        json_node = import_name
    else:
        with open(import_name) as f1:
            json_node = json.load(f1)
    json_node["data"] = json_node.get("data", {})
    if 'data' in json_node.keys():
        if 'buttons' in json_node['data'].keys():
            for node_button in json_node['data'].get("buttons",[]):
                flag = 0
                for root_button in data_merged.get("buttons",[]):
                    if node_button == root_button:
                        flag = 1
                if flag == 0:
                    if 'buttons' in data_merged.keys():
                        data_merged['buttons'].append(node_button)
                    else:
                        data_merged['buttons'] = [node_button]

        if 'overlay_guide' not in data_merged.keys() and 'overlay_guide' in json_node['data'].keys():
            data_merged['overlay_guide'] = json_node['data']['overlay_guide']

        for k in json_node['data'].keys():
            if k not in data_merged.keys():
                data_merged[k] = json_node['data'][k]

    json_root['data'] = data_merged

    return json_root

def merge_entities_caller(json_root, path_head, import_list):
    merged_entities_list = []
    merged_entities_list_final = []
    json_root["entities"] = json_root.get("entities", [])

    for r_node in json_root['entities']:
        check_entity(r_node)

    merged_entities = json_root
    for i in import_list:
        if isinstance(i, dict):
            merged_entities = merge_entities(merged_entities, i)
        else:
            if(path_head!=""):
                merged_entities = merge_entities(merged_entities, i)
            else:
                merged_entities = merge_entities(merged_entities, i)
        merged_entities_list.extend(merged_entities['entities'])

    for e in merged_entities_list:
        if e not in merged_entities_list_final:
            merged_entities_list_final.append(e)


    return merged_entities_list_final

def merge_customer_states_caller(json_root, path_head, import_list):

    merged_customer_states_list = []
    merged_customer_states_list_final = []
    json_root["customer_states"] = json_root.get("customer_states", [])
    for r_node in json_root['customer_states']:
        check_customer_state(r_node)

    merged_customer_states = json_root
    for i in import_list:
        if isinstance(i, dict):
            merged_customer_states = merge_customer_states(merged_customer_states, i)
        else:
            if(path_head!=""):
                merged_customer_states = merge_customer_states(merged_customer_states, i)
            else:
                merged_customer_states = merge_customer_states(merged_customer_states, i)

        merged_customer_states_list.extend(merged_customer_states['customer_states'])

    for e in merged_customer_states_list:
        if e not in merged_customer_states_list_final:
            merged_customer_states_list_final.append(e)


    return merged_customer_states_list_final

def merge_system_responses_caller(json_root, path_head, import_list):
    merged_system_responses_list = []
    merged_system_responses_list_final = []
    json_root["system_responses"] = json_root.get("system_responses", [])
    for r_node in json_root['system_responses']:
        check_system_response(r_node)

    merged_system_responses = json_root
    for i in import_list:
        if isinstance(i, dict):
            merged_system_responses = merge_system_responses(merged_system_responses, i)
        else:
            if(path_head!=""):
                merged_system_responses = merge_system_responses(merged_system_responses, i)
            else:
                merged_system_responses = merge_system_responses(merged_system_responses, i)

        merged_system_responses_list.extend(merged_system_responses['system_responses'])

    for e in merged_system_responses_list:
        if e not in merged_system_responses_list_final:
            merged_system_responses_list_final.append(e)

    # Restrict "nu_parent_nudge" to 5 occurrences
    for sr in merged_system_responses_list_final:
        follow_up_list = []
        nudge_count = 0
        if 'data' in sr.keys() and type(sr['data']) == dict:
            if '_follow_ups' in sr['data'].keys():
                for f in sr['data']['_follow_ups']:
                    if f == "nu_parent_nudge":
                        nudge_count += 1
                    if nudge_count <= 5:
                        follow_up_list.append(f)
                    else:
                        if f != "nu_parent_nudge":
                            follow_up_list.append(f)

            sr['data']['_follow_ups'] = follow_up_list

    return merged_system_responses_list_final

def merge_speech_phrases_caller(json_root, path_head, import_list):
    merged_speech_phrases_final = {}

    json_root["speech_phrases"] = json_root.get("speech_phrases", {})
    merged_speech_phrases = json_root
    for i in import_list:
        if isinstance(i, dict):
            merged_speech_phrases = merge_speech_phrases(merged_speech_phrases, i)
        else:
            if(path_head!=""):
                merged_speech_phrases = merge_speech_phrases(merged_speech_phrases, i)
            else:
                merged_speech_phrases = merge_speech_phrases(merged_speech_phrases, i)


        for sp in merged_speech_phrases['speech_phrases'].keys():
            if sp not in merged_speech_phrases_final.keys():
                merged_speech_phrases_final[sp] = merged_speech_phrases['speech_phrases'][sp]
            else:
                merged_speech_phrases_final[sp].extend(merged_speech_phrases['speech_phrases'][sp])
                merged_speech_phrases_final[sp] = list(set(merged_speech_phrases_final[sp]))

    return merged_speech_phrases_final

def merge_translations_caller(json_root, path_head, import_list):
    merged_translations_final = {}

    json_root["translations"] = json_root.get("translations", [])
    merged_translations = json_root
    for i in import_list:
        if isinstance(i, dict):
            merged_translations = merge_translations(merged_translations, i)
        else:
            if path_head!="":
                merged_translations = merge_translations(merged_translations, i)
            else:
                merged_translations = merge_translations(merged_translations, i)


        merged_translations_final.update(merged_translations['translations'])

    return merged_translations_final

def merge_data_caller(json_root, path_head, import_list):
    merged_data_final = {}

    json_root["data"] = json_root.get("data", {})
    merged_data = json_root
    for i in import_list:
        if isinstance(i, dict):
            merged_data = merge_data(merged_data, i)
        else:
            if path_head!="":
                merged_data = merge_data(merged_data, i)
            else:
                merged_data = merge_data(merged_data, i)


        if 'buttons' in merged_data_final.keys():
            merged_data_final['buttons'].extend(merged_data['data']['buttons'])
        else:
            if 'buttons' in merged_data['data'].keys():
                merged_data_final['buttons'] = merged_data['data']['buttons']

        merged_data_final.update(merged_data['data'])

    buttons_list_final = []

    if 'buttons' in merged_data_final.keys():
        for b in merged_data_final['buttons']:
            if b not in buttons_list_final:
                buttons_list_final.append(b)

    merged_data_final['buttons'] = buttons_list_final

    return merged_data_final

def find_file_path(path,file_name):
    count = 0
    while count < 5:
        file_exists = exists(path+os.sep+file_name)
        if file_exists:
            return path+os.sep+file_name        
        path = os.path.dirname(path)
        count+=1
    return None


def get_imports(conv1):
    import_list = []
    path_head, path_tail = os.path.split(conv1)
    if isinstance(conv1, dict):
        json_root = conv1
    else:
        with open(conv1) as f:
            json_root = json.load(f)

    keys_list = json_root.keys()
    keys_list = list(keys_list)
    if("dave_import" in keys_list):
        current_import_list = json_root.get("dave_import", [])
        current_import_list = [i+"/conversation.json" for i in current_import_list]
        current_import_list = [str(i) for i in current_import_list]
        for i in current_import_list:
            found_file_path = find_file_path(path_head, i)
            if found_file_path:
                import_list.append(found_file_path)
            else :
                continue
            if i == path_tail:  
                exit()
            if(path_head!=""):
                recurse_list = get_imports(found_file_path)
                import_list.extend(recurse_list)
            else:
                recurse_list = get_imports(i)
                import_list.extend(recurse_list)

        import_list = list(import_list)
    return import_list

def merge_conversations(conv1, import_list, func="all"):
    path_head, path_tail = None, None
    if isinstance(conv1, dict):
        json_root = conv1
    else:
        with open(conv1) as f:
            json_root = json.load(f)

        path_head, path_tail = os.path.split(conv1)

        import_list = get_imports(conv1)

    if func == 'entities':
        json_root['entities'] = merge_entities_caller(json_root, path_head, import_list)

    elif func == 'customer_states':
        json_root['customer_states'] = merge_customer_states_caller(json_root, path_head, import_list)

    elif func == 'system_responses':
        json_root['system_responses'] = merge_system_responses_caller(json_root, path_head, import_list)

    elif func == 'speech_phrases':
        json_root['speech_phrases'] = merge_speech_phrases_caller(json_root, path_head, import_list)

    elif func == 'translations':
        json_root['translations'] = merge_translations_caller(json_root, path_head, import_list)

    elif func == 'data':
        json_root['data'] = merge_data_caller(json_root, path_head, import_list)

    elif func == 'all':
        json_root['entities'] = merge_entities_caller(json_root, path_head, import_list)
        json_root['customer_states'] = merge_customer_states_caller(json_root, path_head, import_list)
        json_root['system_responses'] = merge_system_responses_caller(json_root, path_head, import_list)
        json_root['speech_phrases'] = merge_speech_phrases_caller(json_root, path_head, import_list)
        json_root['translations'] = merge_translations_caller(json_root, path_head, import_list)
        json_root['data'] = merge_data_caller(json_root, path_head, import_list)

    if "dave_import" in json_root:
        del json_root['dave_import']

    return json_root



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Merge conversation JSONs")
    parser.add_argument("-f", "--func", help="Merge entities or customer_states or system_responses or speech_phrases or translations or data or all")
    parser.add_argument("-j", "--json_path", help="Path to json")
    args = (parser.parse_args())

    if args.json_path:
        conv1 = args.json_path
    else:
        print("json_path needed")
    

    path_head, path_tail = os.path.split(conv1)
    import_list = get_imports(conv1)
    

    with open(conv1) as f:
        json_root = json.load(f)
    
    if len(import_list):
        if args.func == 'entities':
            json_root['entities'] = merge_entities_caller(json_root, path_head, import_list)

        elif args.func == 'customer_states':
            json_root['customer_states'] = merge_customer_states_caller(json_root, path_head, import_list)

        elif args.func == 'system_responses':
            json_root['system_responses'] = merge_system_responses_caller(json_root, path_head, import_list)

        elif args.func == 'speech_phrases':
            json_root['speech_phrases'] = merge_speech_phrases_caller(json_root, path_head, import_list)

        elif args.func == 'translations':
            json_root['translations'] = merge_translations_caller(json_root, path_head, import_list)

        elif args.func == 'data':
            json_root['data'] = merge_data_caller(json_root, path_head, import_list)

        elif args.func == 'all':
            json_root['entities'] = merge_entities_caller(json_root, path_head, import_list)
            json_root['customer_states'] = merge_customer_states_caller(json_root, path_head, import_list)
            json_root['system_responses'] = merge_system_responses_caller(json_root, path_head, import_list)
            json_root['speech_phrases'] = merge_speech_phrases_caller(json_root, path_head, import_list)
            json_root['translations'] = merge_translations_caller(json_root, path_head, import_list)
            json_root['data'] = merge_data_caller(json_root, path_head, import_list)


    try:
        del json_root['dave_import']
    except:
        pass
    print(json.dumps(json_root, indent=4))
    
    '''print("writing to " ,conv1[:-5]+'_'+args.func+'_merged.json')'''

    with open(conv1[:-5]+'_'+str(args.func)+'_merged.json', 'w') as outfile:
        json.dump(json_root, outfile, indent=4)
       
