"""List of classes helpful everywhere else"""
import inspect
import logging
import copy

# For logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class ResultException(Exception):
    pass


class UtilList(list):
    """Inherits from list class to add unique and duplicate detection functions
    """
    def __init__(self, values=None):
        values = values if values is not None else list()
        super(UtilList, self).__init__(values)

    def unique(self):
        """returns only unique items from the list"""
        return list(set([i.name for i in self]))

    def duplicates(self):
        """returns a dictionary with items and their frequency"""
        return {x: self.count(x.name) for x in self}

    def by_attrib(self, attribute, value):
        """
        To get the first item by attribute and given value of the individual item

        Args:
            value (object): the value of the attribute
            attribute (str): The attribute to check
        """

        for item in self:
            try:
                if eval("item.{attribute}".format(**locals())) == value:
                    result = item
                    raise ResultException
            except AttributeError:
                logger.error("Attribute - {attribute} not found in the object items")
                raise
            except ResultException:
                return result
        return None

    def compare(self, other, attribute):
        """
        To compare two new list item type

        Args:
            attribute (str): Compare which attribute of the list item
            other (UtilList): The object to compare to
        """
        assert isinstance(other, UtilList), "Given object is not of type NewList"
        compare_result = {}
        items_in_self = [eval("item.{attribute}".format(**locals())) for item in self]
        items_in_other = [eval("item.{attribute}".format(**locals())) for item in other]

        extra_items = [item for item in items_in_self if item not in items_in_other]
        missing_items = [item for item in items_in_other if item not in items_in_self]

        for item in self:
            attrib_value = eval("item.{attribute}".format(**locals()))
            if attrib_value in items_in_other:
                other_item = other[attrib_value]
                result = item.compare(other_item)
                if result:
                    compare_result.update({attrib_value: result})

        return compare_result, extra_items, missing_items

    def remove_by_index(self, index):
        """To remove by index

        Args:
            index (int): The index value to remove
        """
        self.__init__([self[index] for idx, _ in enumerate(self) if idx != index])
        pass

    def remove_by_attribute(self, attribute, value):
        """To remove an item from the list, based on the attribute of the item given

        Args:
            attribute (str): The attribute to check
            value (str): The value to remove
        """
        for index, item in enumerate(self[:]):
            if eval("item.{attribute}".format(**locals())) == value:
                self.remove_by_index(index)
                return True
        else:
            logger.warning("UtilList.remove_by_attribute: {value} not in list item".format(**locals()))
            return False

    def __contains__(self, item):
        """To check if the item exist in the list"""
        try:
            return item in [i.name for i in self]
        except AttributeError:
            return super(UtilList, self).__contains__(item)

    def __getitem__(self, item):
        """Can be used to get item by name while still preserving the index"""
        if isinstance(item, str):
            for element in self:
                if element.name == item:
                    return element
        else:
            return super(UtilList, self).__getitem__(item)

    def __setitem__(self, key, value):
        """Can be used to set item by name while still preserving the index"""
        self[key] = value


def str2digit(string):
    """
    To convert string to a numeric value

    Args:
        string: the string value to be converted

    Returns:
        val: converted value
    """
    if isinstance(string, str):
        try:
            val = int(string)
        except ValueError:
            try:
                val = float(string)
                val = float_or_int(val)
            except ValueError:
                try:
                    val = int(string, 16)
                except ValueError:
                    val = string
        return val
    else:
        return string


def float_or_int(value):
    """
    To check if the given value is really float or int. If it is int it returns an int type value

    Args:
        value (Union(int, float)): The value to check

    Returns:
        Union(int,float): The value converted to int if possible
    """
    assert isinstance(value, (int, float)), "The given value is not int or float is instead {}".format(type(value))
    return int(value) if int(value) == value else value


def compare_dict(this, other):
    """
    To compare two dicts containing values of DBC type classes or normal dict

    Args:
        this (dict): Object to compare
        other (dict): The object to compare to
    """
    assert isinstance(other, dict), "Given object is not of type dict"
    compare_result = {}
    items_in_self = this.keys()
    items_in_other = other.keys()

    extra_items = [item for item in items_in_self if item not in items_in_other]
    missing_items = [item for item in items_in_other if item not in items_in_self]

    for item_name, item in this.iteritems():
        if item_name in items_in_other:
            other_item = other[item_name]
            if hasattr(item, "compare"):
                result = item.compare(other_item)
                if result:
                    compare_result.update({item_name: result})
            else:
                if item != other_item:
                    compare_result.update({item_name: [item, other_item]})

    return compare_result, extra_items, missing_items


class _Object(object):
    """For testing"""
    pass


class VarContainer(object):
    @classmethod
    def members(cls):
        members = []
        for key, value in cls.__dict__.iteritems():
            if not cls.__dunder__(key):
                members.append(value)
        return members

    @staticmethod
    def __dunder__(key):
        if key.startswith("__") and key.endswith("__"):
            return True
        return False
