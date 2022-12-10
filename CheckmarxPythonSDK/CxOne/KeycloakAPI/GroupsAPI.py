import json
from ...utilities.compat import CREATED, NO_CONTENT
from ..httpRequests import get_request, post_request, put_request, delete_request
from typing import List
from ..utilities import get_url_param, type_check
from .url import api_url

from CheckmarxPythonSDK.CxOne.KeycloakAPI.dto import (
    Group,
    construct_group,
    GroupRepresentation,
)


def get_group_hierarchy(realm, brief_representation=False, first=None, max_result_size=100, search=None) -> List[Group]:
    """
    Get group hierarchy.
    Args:
        realm (str):
        brief_representation (bool):
        first (int):
        max_result_size (int):
        search (str):

    Returns:
        List[Group]
    """
    type_check(realm, str)
    type_check(brief_representation, bool)
    type_check(first, str)
    type_check(max_result_size, int)
    type_check(search, str)

    relative_url = api_url + f"/{realm}/groups"
    relative_url += "?"
    relative_url += get_url_param("briefRepresentation", brief_representation)
    relative_url += get_url_param("first", first)
    relative_url += get_url_param("max", max_result_size)
    relative_url += get_url_param("search", search)
    response = get_request(relative_url=relative_url, is_iam=True)
    response = response.json()
    groups = [construct_group(item) for item in response]
    return groups


def create_group_set(realm, group_representation) -> bool:
    """
    create or add a top level realm groupSet or create child.
    Args:
        realm (str):
        group_representation (GroupRepresentation):

    Returns:
        bool (True for success, False for failure)
    """
    result = False
    type_check(realm, str)
    type_check(group_representation, GroupRepresentation)
    relative_url = api_url + f"/{realm}/groups"
    post_data = group_representation.get_post_data()
    response = post_request(relative_url=relative_url, data=post_data, is_iam=True)
    if response.status_code == CREATED:
        result = True
    return result


def get_group_by_name(realm, group_name) -> Group:
    """

    Args:
        realm (str):
        group_name (str):

    Returns:
        Group
    """
    result = None
    type_check(realm, str)
    type_check(group_name, str)
    groups = get_group_hierarchy(realm=realm, max_result_size=1000)
    one_group = list(filter(lambda g: g.name == group_name, groups))
    if len(one_group) == 1:
        result = one_group[0]
    return result


def get_number_of_groups_in_a_realm(realm) -> int:
    """
    Returns the groups counts.
    Args:
        realm (str):

    Returns:
        int
    """
    type_check(realm, str)
    relative_url = api_url + f"/{realm}/groups/count"
    response = get_request(relative_url=relative_url, is_iam=True)
    response = response.json()
    result = response.get("count")
    return result


def get_group_by_id(realm, group_id) -> Group:
    """

    Args:
        realm (str):
        group_id (str):

    Returns:

    """
    type_check(realm, str)
    type_check(group_id, str)
    relative_url = api_url + f"/{realm}/groups/{group_id}"
    response = get_request(relative_url=relative_url, is_iam=True)
    item = response.json()
    return construct_group(item)


def update_group_by_id(realm, group_id, group_representation) -> bool:
    """

    Args:
        realm (str):
        group_id (str):
        group_representation (GroupRepresentation):

    Returns:
        bool
    """
    result = False
    type_check(realm, str)
    type_check(group_id, str)
    relative_url = api_url + f"/{realm}/groups/{group_id}"
    type_check(group_representation, GroupRepresentation)
    post_data = group_representation.get_post_data()
    response = put_request(relative_url=relative_url, data=post_data, is_iam=True)
    if response.status_code == NO_CONTENT:
        result = True
    return result


def delete_group_by_id(realm, group_id) -> bool:
    """

    Args:
        realm (str):
        group_id (str):

    Returns:

    """
    result = False
    type_check(realm, str)
    type_check(group_id, str)
    relative_url = api_url + f"/{realm}/groups/{group_id}"
    response = delete_request(relative_url=relative_url, is_iam=True)
    if response.status_code == NO_CONTENT:
        result = True
    return result


def create_subgroup(realm, group_id, subgroup_name):
    """
    Set or create child.
    Args:
        realm (str):
        group_id (str):
        subgroup_name (str):

    Returns:
        bool
    """
    result = False
    type_check(realm, str)
    type_check(group_id, str)
    type_check(subgroup_name, str)
    relative_url = api_url + f"/{realm}/groups/{group_id}/children"
    post_data = json.dumps(
        {
            'name': subgroup_name
        }
    )
    response = post_request(relative_url=relative_url, data=post_data, is_iam=True)
    if response.status_code == CREATED:
        result = True
    return result


def get_group_permissions(realm, group_id):
    pass


def update_group_permissions(realm, group_id):
    pass


def get_group_members(realm, group_id):
    pass


def create_group(realm, group_name):
    """

    Args:
        realm (str):
        group_name (str):

    Returns:
        bool
    """
    result = False
    type_check(realm, str)
    type_check(group_name, str)
    relative_url = api_url + f"/{realm}/groups"
    post_data = json.dumps(
        {
            'name': group_name
        }
    )
    response = post_request(relative_url=relative_url, data=post_data, is_iam=True)
    if response.status_code == CREATED:
        result = True
    return result
