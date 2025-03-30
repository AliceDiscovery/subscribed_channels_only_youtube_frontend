""" implements a base class for all data classes """
from abc import ABC
from inspect import stack, currentframe


class DatatypeABC(ABC):
    """ implements a base class for all data classes """
    def _validate_setter_type(self, value, valid_types: list|set|tuple, attribute_name: str=None):
        """ allows type validation for setter input values. """
        def raise_error(attribute_name: str, value, valid_types):
            type_names = [t.__name__ if t is not None else 'None' for t in valid_types]

            types_string = '|'.join(set(type_names))
            indefinite_article = 'an' if types_string[0].lower() in 'aeiou' else 'a'

            if types_string and types_string[0].lower() in {'a', 'e', 'i', 'o', 'u'}:
                indefinite_article = 'an'
            else:
                indefinite_article = 'a'

            try:
                actual_type = value.__name__
            except AttributeError:
                actual_type = type(value).__name__

            msg = f'{attribute_name} must be {indefinite_article} {types_string}; not {actual_type}'
            raise ValueError(msg)

        if not any(isinstance(valid_types, _type) for _type in (list, set, tuple)):
            raise_error('valid_types', valid_types, {list, set, tuple})
        if not valid_types:
            raise ValueError('valid_types argument must contain at least one element')

        if value is None and None in valid_types:
            return

        if not any(isinstance(value, _type) for _type in valid_types if _type is not None):
            if attribute_name is not None:
                raise_error(str(attribute_name), value, valid_types)
            raise_error(f'{self.__class__.__name__}.{stack()[1].function}', value, valid_types)

    def _validate_argument_type(self, variable, valid_types: list|set|tuple):
        """ allows type validation for function input arguments """
        for variable_name, variable_val in currentframe().f_back.f_locals.items():
            if variable_val is variable:
                self._validate_setter_type(
                    value=variable,
                    valid_types=valid_types,
                    attribute_name=variable_name
                )
                break
        else:
            raise ValueError('Variable name can not be found.')

    def _serialize_data(self) -> dict:
        properties = {}
        for attribute in dir(self):
            if not attribute.startswith('_'):
                if isinstance(getattr(self.__class__, attribute), property):
                    properties[attribute] = getattr(self, attribute)
        return properties

    def __repr__(self):
        properties = self._serialize_data()
        properties_str = ', '.join(f'{key}={value!r}' for key, value in properties.items())
        return f'{self.__class__.__name__}({properties_str})'
