import json
import pprint

import mongoengine as mEngine
from phantom.application_settings import settings

class schema():
    def __init__(self, coll_name, schema_json=None, ref_schemas=None):
        self.__schema_json = schema_json
        self.__ref_schemas = ref_schemas

        self.__schema_cls = None
        self.__ref_schema_cls_dict = {}

        self.__coll_name = coll_name

    def build_document(self, doc, schema_cls=None, level=0):
        empty_doc_flag = True
        new_doc = schema_cls
        tmp = {}
        if not schema_cls:
            schma = self.get_schema_cls()
            new_doc = schma()
        if level == 0:
            tmp = json.loads(self.__schema_json)
        for field in doc:
            if hasattr(new_doc, field):
                if level == 0 and (tmp[field].get("type") == "EmbeddedDocument" or tmp[field].get("type") == "Reference"):
                    setattr(new_doc, field, self.build_document(doc[field], self.__ref_schema_cls_dict[tmp[field]["document_type"]](), level+1))
                else:
                    setattr(new_doc, field, doc[field])
                empty_doc_flag = False

        if empty_doc_flag:
            return None

        return new_doc

    def get_schema_cls(self, schma="Main"):
        if schma == "Main" and not self.__schema_cls:
            return self.__mk_schema_cls(self.__coll_name, mEngine.Document, self.__schema_json)
        else:
            return self.__schema_cls

    def get_ref_schema_cls_dict(self):
        return self.__ref_schema_cls_dict

    def __mk_schema_cls(self, collection, super_cls, schema_json):
        try:
            return type(collection, (super_cls, ), self.__mk_attribute_dict(json.loads(schema_json)))
        except (json.decoder.JSONDecodeError, TypeError) as err:
            settings.__LOG__.logError("JSON_ERR: " + str(err))
            return None

    def set_schema_json(self, new_schema):
        self.__schema_json = new_schema
        self.__schema_cls = self.__mk_schema_cls(self.__coll_name, mEngine.Document, self.__schema_json)

    def get_schema_json(self):
        return self.__schema_json

    def set_connection(self, db, host, port, username=None, password=None, auth_src=None):
        mEngine.connect(db=db, host=host, port=port, username=username, password=password,
                        authentication_source=auth_src)

    def __mk_attribute_dict(self, attr_set):
        attribute_dict = {}

        for key in attr_set:
            attribute_dict[key] = self.get_field(attr_set[key]["type"], attr_set, key)

        return attribute_dict

    def get_field(self, field_str, attr_set={}, doc_type=None):
        if field_str == "String":
            return self.string_field(attr_set)
        elif field_str == "Integer":
            return self.integer_field(attr_set)
        elif field_str == "Boolean":
            return self.boolean_field(attr_set)
        elif field_str == "List":
            return self.list_field(attr_set)
        elif field_str == "Dict":
            return self.dict_field(attr_set)
        elif field_str == "EmbeddedDocument":
            return self.embedded_document_field(attr_set, doc_type)
        elif field_str == "Reference":
            return self.reference_field(attr_set)
        else: return None

    def string_field(self, attrs_dict):
        return mEngine.StringField(regex=attrs_dict.get("regex"), max_length=attrs_dict.get("max_length"), min_length=attrs_dict.get("min_length"),
                    db_field=attrs_dict.get("db_field"), required=string_to_bool(attrs_dict.get("required")), default=self.get_type(attrs_dict.get("default")),
                    unique=attrs_dict.get("unique"), unique_with=attrs_dict.get("unique_with"), primary_key=string_to_bool(attrs_dict.get("primary_key")),
                    validation=attrs_dict.get("validation"), choices=attrs_dict.get("choices"), null=attrs_dict.get("null"))

    def integer_field(self, attrs_dict):
        return mEngine.IntField(max_value=attrs_dict.get("max_value"), min_value=attrs_dict.get("min_value"),
                    db_field=attrs_dict.get("db_field"), required=string_to_bool(attrs_dict.get("required")), default=self.get_type(attrs_dict.get("default")),
                    unique=attrs_dict.get("unique"), unique_with=attrs_dict.get("unique_with"), primary_key=string_to_bool(attrs_dict.get("primary_key")),
                    validation=attrs_dict.get("validation"), choices=attrs_dict.get("choices"), null=attrs_dict.get("null"))

    def list_field(self, attrs_dict):
        return mEngine.ListField(field=(self.get_field(attrs_dict.get("field"))),
                    db_field=attrs_dict.get("db_field"), required=string_to_bool(attrs_dict.get("required")), default=self.get_type(attrs_dict.get("default")),
                    unique=attrs_dict.get("unique"), unique_with=attrs_dict.get("unique_with"), primary_key=string_to_bool(attrs_dict.get("primary_key")),
                    validation=attrs_dict.get("validation"), choices=attrs_dict.get("choices"), null=attrs_dict.get("null"))

    def dict_field(self, attrs_dict):
        return mEngine.DictField(field=attrs_dict.get("field"),
                    db_field=attrs_dict.get("db_field"), required=string_to_bool(attrs_dict.get("required")), default=self.get_type(attrs_dict.get("default")),
                    unique=attrs_dict.get("unique"), unique_with=attrs_dict.get("unique_with"), primary_key=string_to_bool(attrs_dict.get("primary_key")),
                    validation=attrs_dict.get("validation"), choices=attrs_dict.get("choices"), null=attrs_dict.get("null"))

    def boolean_field(self, attrs_dict):
        return mEngine.BooleanField(db_field=attrs_dict.get("db_field"), required=string_to_bool(attrs_dict.get("required")), default=self.get_type(attrs_dict.get("default")),
                            unique=attrs_dict.get("unique"), unique_with=attrs_dict.get("unique_with"), primary_key=string_to_bool(attrs_dict.get("primary_key")),
                            validation=attrs_dict.get("validation"), choices=attrs_dict.get("choices"), null=attrs_dict.get("null"),
                            sparse=attrs_dict.get("sparse"))

    def embedded_document_field(self, attrs_dict, key):
        if not self.__ref_schemas.get(attrs_dict.get("document_type")):
            setattr(attrs_dict, "document_type", key)
            # raise Exception("no schema for given document type " + str(attrs_dict.get("document_type")))
        if not self.__ref_schema_cls_dict.get(attrs_dict.get("document_type")):
            self.__ref_schema_cls_dict[attrs_dict.get("document_type")] = self.__mk_schema_cls(attrs_dict.get("document_type"), mEngine.EmbeddedDocument, self.__ref_schemas.get(attrs_dict.get("document_type")))
        
        return mEngine.EmbeddedDocumentField(document_type=self.__ref_schema_cls_dict[attrs_dict.get("document_type")], db_field=attrs_dict.get("db_field"), required=string_to_bool(attrs_dict.get("required")),
                                    default=self.get_type(attrs_dict.get("default")), unique=attrs_dict.get("unique"), unique_with=attrs_dict.get("unique_with"),
                                    primary_key=string_to_bool(attrs_dict.get("primary_key")), validation=attrs_dict.get("validation"), choices=attrs_dict.get("choices"),
                                    null=attrs_dict.get("null"))

    def reference_field(self, attrs_dict):
        if not self.__ref_schemas.get(attrs_dict.get("document_type")):
            raise Exception("no schema for given document type")

        db_ref = False
        rd_rule = 0

        if attrs_dict.get("dbref"):
            db_ref = attrs_dict["dbref"]
        if attrs_dict.get("reverse_delete_rule"):
            rd_rule = attrs_dict["reverse_delete_rule"]

        if not self.__ref_schema_cls_dict.get(attrs_dict.get("document_type")):
            self.__ref_schema_cls_dict[attrs_dict.get("document_type")] = self.__mk_schema_cls(attrs_dict.get("document_type"), mEngine.Document, self.__ref_schemas.get(attrs_dict.get("document_type")))

        return mEngine.ReferenceField(document_type=self.__ref_schema_cls_dict[attrs_dict.get("document_type")], dbref=db_ref, reverse_delete_rule=rd_rule,
                            db_field=attrs_dict.get("db_field"), required=string_to_bool(attrs_dict.get("required")), default=self.get_type(attrs_dict.get("default")),
                            unique=attrs_dict.get("unique"), unique_with=attrs_dict.get("unique_with"), primary_key=string_to_bool(attrs_dict.get("primary_key")),
                            validation=attrs_dict.get("validation"), choices=attrs_dict.get("choices"), null=attrs_dict.get("null"))


    def get_type(self, val):
        if val is None or val.lower() == "none":
            return None

def string_to_bool(string):
    if string is None:
        return None
    elif string.lower() == "false":
        return False
    elif string.lower() == "true":
        return True
    else:
        raise IOError
