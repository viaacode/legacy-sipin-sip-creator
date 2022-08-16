#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import Enum
from typing import List

from lxml import etree

from app.helpers.xml_utils import qname_text


NSMAP = {
    "premis": "http://www.loc.gov/premis/v3",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
}


class ObjectCategoryType(Enum):
    IE = "intellectual entity"
    FILE = "file"
    REPRESENTATION = "representation"


class RelationshipSubtype(Enum):
    INCLUDES = "includes"
    REPRESENTED_BY = "is represented by"
    REPRESENTS = "represents"
    INCLUDED_IN = "is included in"


class ObjectType(Enum):
    IE = "intellectualEntity"
    FILE = "file"
    REPRESENTATION = "representation"


class OriginalName:
    """Class representing a originalName node.

    Args:
        name: The original name."""

    def __init__(self, name: str):
        self.name = name

    def to_element(self):
        """Returns the originalName node as an lxml element.

        Returns:
            The originalName element."""

        # Premis original name
        original_name_element = etree.Element(
            qname_text(NSMAP, "premis", "originalName")
        )
        original_name_element.text = self.name

        return original_name_element


class ObjectIdentifier:
    """Class representing a objectIdentifier node.

    Args:
        type: The type of the object identifier.
        value: The value of the object identifier."""

    def __init__(self, type: str, value: str):
        self.type = type
        self.value = value

    def to_element(self):
        """Returns the objectIdentifier node as an lxml element.

        Returns:
            The objectIdentifier element."""

        # Premis object identifier
        object_identifier_element = etree.Element(
            qname_text(NSMAP, "premis", "objectIdentifier")
        )
        # Premis related object identifier
        etree.SubElement(
            object_identifier_element,
            qname_text(NSMAP, "premis", "objectIdentifierType"),
        ).text = self.type
        # Premis related object identifier value
        etree.SubElement(
            object_identifier_element,
            qname_text(NSMAP, "premis", "objectIdentifierValue"),
        ).text = self.value

        return object_identifier_element


class RelatedObjectIdentifier:
    """Class representing a relatedObjectIdentifier node.

    Args:
        uuid: The uuid."""

    def __init__(self, uuid: str):
        self.uuid = uuid

    def to_element(self):
        """Returns the relatedObjectIdentifier node as an lxml element.

        Returns:
            The relatedObjectIdentifier element."""

        # Premis related object identifier
        object_identifier_element = etree.Element(
            qname_text(NSMAP, "premis", "relatedObjectIdentifier")
        )
        # Premis related object identifier type
        etree.SubElement(
            object_identifier_element,
            qname_text(NSMAP, "premis", "relatedObjectIdentifierType"),
        ).text = "UUID"
        # Premis related object identifier value
        etree.SubElement(
            object_identifier_element,
            qname_text(NSMAP, "premis", "relatedObjectIdentifierValue"),
        ).text = self.uuid

        return object_identifier_element


class Relationship:
    """Class representing a relationship node.

    Args:
        subtype: The subtype of the relationship.
        uuid: The uuid.
    """

    TYPE_URI_MAP = {
        RelationshipSubtype.INCLUDES: "inc",
        RelationshipSubtype.REPRESENTED_BY: "isr",
        RelationshipSubtype.REPRESENTS: "rep",
        RelationshipSubtype.INCLUDED_IN: "isi",
    }

    def __init__(self, subtype: RelationshipSubtype, uuid: str):
        self.subtype = subtype
        self.uuid = uuid

    def to_element(self):
        """Returns the relationship node as an lxml element.

        Returns:
            The relationship element."""

        # Premis relationship
        relationship_element = etree.Element(
            qname_text(NSMAP, "premis", "relationship")
        )
        # type
        relationship_type_attributes = {
            "authority": "relationshipType",
            "authorityURI": "http://id.loc.gov/vocabulary/preservation/relationshipType",
            "valueURI": "http://id.loc.gov/vocabulary/preservation/relationshipType/str",
        }
        etree.SubElement(
            relationship_element,
            qname_text(NSMAP, "premis", "relationshipType"),
            attrib=relationship_type_attributes,
        ).text = "structural"

        # Subtype
        relationship_subtype_attributes = {
            "authority": "relationshipSubType",
            "authorityURI": "http://id.loc.gov/vocabulary/preservation/relationshipSubType",
            "valueURI": f"http://id.loc.gov/vocabulary/preservation/relationshipSubType/{self.TYPE_URI_MAP[self.subtype]}",
        }
        etree.SubElement(
            relationship_element,
            qname_text(NSMAP, "premis", "relationshipSubtype"),
            attrib=relationship_subtype_attributes,
        ).text = self.subtype.value

        # Related object identifier
        relationship_element.append(RelatedObjectIdentifier(self.uuid).to_element())

        return relationship_element


class Fixity:
    """Class representing the Fixity information contained in a ObjectCharacteristics node.

    Args:
        md5: The md5.
    """

    def __init__(self, md5: str = None):
        self.md5 = md5

    def to_element(self):
        """Returns the fixity node as an lxml element.

        If the md5 value is empty, the fixity node will be empty.

        Returns:
            The Premis fixity element."""

        # Premis object characteristics
        object_characteristics_element = etree.Element(
            qname_text(NSMAP, "premis", "objectCharacteristics"),
        )
        fixity_element = etree.SubElement(
            object_characteristics_element,
            qname_text(NSMAP, "premis", "fixity"),
        )
        if self.md5:
            etree.SubElement(
                fixity_element,
                qname_text(NSMAP, "premis", "messageDigestAlgorithm"),
                attrib={
                    "authority": "cryptographicHashFunctions",
                    "authorityURI": "http://id.loc.gov/vocabulary/preservation/cryptographicHashFunctions",
                    "valueURI": "http://id.loc.gov/vocabulary/preservation/cryptographicHashFunctions/md5",
                },
            ).text = "MD5"
            etree.SubElement(
                fixity_element,
                qname_text(NSMAP, "premis", "messageDigest"),
            ).text = self.md5

        return object_characteristics_element


class ObjectCategory:
    """Class representing a objectCategory node.

    Args:
        category: The category."""

    def __init__(self, category: ObjectCategoryType):
        self.category = category

    def to_element(self):
        """Returns the objectCategory node as an lxml element.

        Returns:
            The objectCategory element."""

        # Premis object category
        object_category_element = etree.Element(
            qname_text(NSMAP, "premis", "objectCategory"),
        )
        object_category_element.text = self.category.value

        return object_category_element


class Object:
    """Class representing a object node.

    Args:
        type: The object type.
        identifiers: The object identifiers.
        original_name: The original name.
        fixity: The fixity element.
        relationships: The relationships.
    """

    def __init__(
        self,
        type: ObjectType,
        identifiers: List[ObjectIdentifier],
        original_name: str = None,
        fixity: Fixity = None,
        relationships: List[Relationship] = None,
    ):
        self.type: ObjectType = type
        self.identifiers = identifiers
        self.original_name = original_name
        self.fixity = fixity
        self.relationships = relationships if relationships else []

    def add_relationship(self, relationship: Relationship):
        self.relationships.append(relationship)

    def add_identifier(self, identifier: ObjectIdentifier):
        self.identifiers.append(identifier)

    def to_element(self):
        """Returns the object node as an lxml element.

        Returns:
            The object element."""

        # Premis object
        object_attributes = {
            qname_text(NSMAP, "xsi", "type"): f"premis:{self.type.value}"
        }
        object_element = etree.Element(
            qname_text(NSMAP, "premis", "object"), attrib=object_attributes
        )

        # Premis original name
        if self.original_name:
            object_element.append(OriginalName(self.original_name).to_element())

        # Premis object identifiers
        for identifier in self.identifiers:
            object_element.append(identifier.to_element())

        # Premis fixity
        if self.fixity:
            object_element.append(self.fixity.to_element())

        # Premis relationships
        for relationship in self.relationships:
            object_element.append(relationship.to_element())

        return object_element


class Premis:
    """Class representing the premis root node."""

    ATTRS = {"version": "3.0"}

    def __init__(self):
        self.objects: Object = []

    def add_object(self, object: Object):
        self.objects.append(object)

    def to_element(self):
        """Returns the premis node as an lxml element.

        Returns:
            The premis element."""

        # Premis premis
        premis_element = etree.Element(
            qname_text(NSMAP, "premis", "premis"), nsmap=NSMAP, attrib=self.ATTRS
        )
        # Add the objects
        for obj in self.objects:
            premis_element.append(obj.to_element())

        return premis_element
