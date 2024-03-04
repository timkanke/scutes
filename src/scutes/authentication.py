from djangosaml2.backends import Saml2Backend


class ModifiedSaml2Backend(Saml2Backend):
    def _update_user(self, user, attributes: dict, attribute_mapping: dict, force_save: bool = False):
        if 'eduPersonEntitlement' in attributes:
            groups = [g.lower() for g in attributes['eduPersonEntitlement']]
            if 'scutes-administrator' in groups:
                user.is_staff = True
                user.is_superuser = True
                force_save = True
            elif 'scutes-user' in groups:
                user.is_staff = True
                user.is_superuser = False
                force_save = True
            else:
                user.is_staff = False
                user.is_superuser = False
                force_save = True
        return super()._update_user(user, attributes, attribute_mapping, force_save)
