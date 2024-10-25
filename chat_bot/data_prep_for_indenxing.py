def flatten_info(info):
    """Flatten the dataflow information for embedding."""
    flat_info_for_embedding = list(tuple())
    flat_info_for_embedding.extend(flatten_name_and_description(info))
    flat_info_for_embedding.extend(flatten_dimensions(info))
    flat_info_for_embedding.extend(flatten_codes(info))
    flat_info_for_embedding.extend(get_dataflow_struct_questions(info))

    return flat_info_for_embedding


def flatten_name_and_description(info):

    return [
          ("The Table's name", info.df_name)
        , (info.df_name, "The Table's name")
        , ("The Table's description", info.df_description)
        , (info.df_description, "The Table's description")
    ]


def flatten_dimensions(info):
    ans = []
    for code, name in info.df_dimension_names.items():
        meta_statement = f"The name that corresponds to the column code: '{code}' is {name}."
        ans.append((code, meta_statement))
        ans.append((name, meta_statement))
        ans.append((f"What name corresponds to the column code: '{code}'?", meta_statement))
        ans.append((f"What is the column code for '{name}'?", meta_statement))
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


def get_dataflow_struct_questions(info):
    """
    If we want generic questions about the schema to be searchable, we need to put them explicitly in the vectorstore. 
    The two example use case here are when, the user asks for:
        1. All the columns in the data table.
        2. All the categories (codes) in a specific column.
    """

    ans = []
    ans.append((   "What are the columns in this Tables?"
                , f"These are all the dimension codes and associated English names in this DataFlow: {info.df_dimension_names}"))
   
    for dim_code, dim_name in info.df_dimension_names.items():
        try:
            ans.append((  f"What are all the categories in the column: '{dim_code}'?"
                        , f"""All codes and their English names corresponding to the dimension code: '{dim_code}' and dimension name '{dim_name}' are the follworing: 
                          '''{info.df_code_names[dim_code]}'''.
                          """))
            ans.append((  f"What are all the categories in the column: '{dim_name}'?"
                        , f"""All codes and their English names corresponding to the dimension code: '{dim_code}' and dimension name '{dim_name}' are the follworing: 
                          '''{info.df_code_names[dim_code]}'''.
                          """))
        except:
            print(f"{dim_code} not found in the code names.")

    return ans