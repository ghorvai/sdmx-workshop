def flatten_info(info):
    """Flatten the dataflow information for embedding."""
    flat_info_for_embedding = list(tuple())
    flat_info_for_embedding.extend(flatten_name_and_description(info))
    flat_info_for_embedding.extend(flatten_dimensions(info))
    flat_info_for_embedding.extend(flatten_codes(info))

    return flat_info_for_embedding


def flatten_name_and_description(info):

    return [
          ("The DataFrame's name", info.df_name)
        , (info.df_name, "The DataFrame's name")
        , ("The DataFrame's description", info.df_description)
        , (info.df_description, "The DataFrame's description")
    ]

def flatten_dimensions(info):
    ans = []
    for code, name in info.df_dimension_names.items():
        meta_statement = f"The name that corresponds to the dimension code: '{code}' is {name}."
        ans.append((code, meta_statement))
        ans.append((name, meta_statement))
        ans.append((f"What name corresponds to the dimension code: '{code}'?", meta_statement))
        ans.append((f"What is the dimension code for '{name}'?", meta_statement))
    return ans

def flatten_codes(info):
    ans = []
    for code_list_id in info.df_code_names:
        for code, name in info.df_code_names[code_list_id].items():
            meta_statement = f"The English name of the code '{code}' within the code list ID '{code_list_id}' is '{name}'."
            ans.append((code, meta_statement))
            ans.append((name, meta_statement))
            ans.append((f"What is the English name of the code '{code}' within the code list ID '{code_list_id}'?", meta_statement))
            ans.append((f"What is the code for '{name}' within the code list ID '{code_list_id}'?", meta_statement))
    return ans