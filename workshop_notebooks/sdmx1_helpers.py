import sdmx
import functools
import io
import sys

def suppress_warnings(func):
    """
    This decorator suppresses the output of a function.
    It is useful when you want to suppress the output of a function that prints to stdout
    but you still want to use the return value of the function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Redirect stderr to a string buffer
        old_stderr = sys.stderr
        sys.stderr = io.StringIO()
        
        try:
            # Call the original function
            result = func(*args, **kwargs)
        finally:
            # Restore stderr
            sys.stderr = old_stderr
        
        return result
    return wrapper


@suppress_warnings
def get_metadata_for_full_list_of_dataflows(organization:str)->dict:
    """
    This function will return a dictionary of dataflows for a given organization.
    The dictionary will have the following structure:
    {organization: {dsd_id: {dataflow_name: "name", dsd_urn: "urn", id: 0}}}
    e.g.:organization = "OECD"
    """
    dataflow_meta = dict()
    
    #for i, a in enumerate(sdmx.Client(organization).get("dataflow", detail="full").dataflow.items()):
    # id, name = a    
    for id, name in sdmx.Client(organization).get("dataflow", detail="full").dataflow.items():
        agency = name.maintainer.__str__()
        try:
            dataflow_name = name.name['en'] # of course: AttributeError: 'DataflowDefinition' object has no attribute 'get' 🙄
        except:
            dataflow_name = None
        dsd_id = name.structure.id
        dsd_urn = name.structure.urn  # what does this urn identify??

        # Handle the case where the agency is not in the dictionary
        if agency not in dataflow_meta:
            dataflow_meta[agency] = dict()

        dataflow_meta[agency][dsd_id] = {"dataflow_name": dataflow_name, "dsd_urn": dsd_urn, "id": id}
    return dataflow_meta


def restructure_dataflow_meta_dict(data:dict)->dict:
    """
    This function restructures the dictionary returned by get_metadata_for_full_list_of_dataflows() to reflect the hierarchical structure based on the keys. 

    The hierarchy dictionary will have nested dictionaries representing the hierarchy of the keys.
    E.g. OECD.WISE.WDP will be represented as {'OECD': {'WISE': {'WDP': {}}}} to reflect the the organization, directorate, and domain levels.
    """
    hierarchy = {}

    for key, value in data.items():
        parts = key.split('.')
        current_level = hierarchy
        
        for part in parts[:-1]:
            if part not in current_level:
                current_level[part] = {}
            current_level = current_level[part]
        
        current_level[parts[-1]] = value

    return hierarchy


def _get_dimension_information(dsd_id:str, dataflow_id:str)->list[dict[str,str]]:
    """
    Data_Structure_Definition_id and DataFlow_id are required to get the dimension information of the dataflow.
    """

    dims = sdmx.Client("OECD").datastructure(dsd_id).dataflow[dsd_id + '@' + dataflow_id].structure.dimensions.components
    dimensions = list()
    for dim in dims:
        dimension_info = dict()
        dimension_info['dim_code'] = dim.concept_identity.id
        dimension_info['dim_name'] = dim.concept_identity.name['en']
        try:
            dimension_info['corresponding_codelist'] = dim.concept_identity.core_representation.enumerated.id
        except:
            dimension_info['corresponding_codelist'] = None
        dimensions.append(dimension_info)
        
    return dimensions


def get_dimension_information(dsd_id:str, dataflow_id:str)->list[dict[str,str]]:
    """
    Data_Structure_Definition_id and DataFlow_id are required to get the dimension information of the dataflow.
    """

    dims = sdmx.Client("OECD").datastructure(dsd_id).dataflow[dsd_id + '@' + dataflow_id].structure.dimensions.components
    dimensions = dict()
    for dim in dims:
        try:
            corresponding_codelist = dim.concept_identity.core_representation.enumerated.id
        except:
            corresponding_codelist = None

        dimensions[dim.concept_identity.id] = {  "name": dim.concept_identity.name['en']
                                               , "codelist": corresponding_codelist}
        
    return dimensions


def get_agencies(organization:str)->dict:
    """
    
    """

    agencies = dict()
    agency_items = sdmx.Client(organization).get("agencyscheme").organisation_scheme[organization +':AGENCIES'].items
    for agency_code in agency_items:
        agencies[agency_code] = agency_items[agency_code].name.__str__()
    return agencies


def get_dataflow_constraint_ids(organisation:str)->dict:
    contentconstraints = sdmx.Client(organisation).get("contentconstraint").constraint
    dataflow_constraint_ids = {}
    for constraint_id in contentconstraints:
        try:
            c_id, df_id = constraint_id.split("@")
            version = contentconstraints[constraint_id].version
            if df_id not in dataflow_constraint_ids:
                dataflow_constraint_ids[df_id] = {version: c_id}
            else:
                dataflow_constraint_ids[df_id][version] = c_id
        except:
            pass
        #print(f"{constraint_id:38} : {constraint_obj.name}")
    return dataflow_constraint_ids

def get_dataflow_constraint_ids_single_version(organisation:str)->dict:
    """
    Though there are multiple versions of constraints for a dataflow, this function will return only the latest version of the constraint for each dataflow.
    Since it seems that the latest version is the default and we can't access the previous versions.
    The dictionary will have the following structure:
    {dataflow_id: constraint_id}
    """
    
    contentconstraints = sdmx.Client(organisation).get("contentconstraint").constraint
    dataflow_constraint_ids = {}
    for constraint_id in contentconstraints:
        try:
            c_id, df_id = constraint_id.split("@")
            dataflow_constraint_ids[df_id] = c_id
        except:
            pass

    return dataflow_constraint_ids


def get_constrained_codelists_by_dimensions(organisation, dsd_id, dataflow_id, constraint_id):
    """
    had to dig deep for this one ...
    """
    
    constrained_codelists_by_dimensions = dict()
    for id, selection in sdmx.Client(organisation).dataflow(dsd_id + '@' + dataflow_id).constraint[constraint_id + '@' + dataflow_id].data_content_region[0].member.items():
        # selection.values_for.id == id.id ... whatever a this point ...
        constrained_codelists_by_dimensions[id.id] = selection.values
    
    return constrained_codelists_by_dimensions