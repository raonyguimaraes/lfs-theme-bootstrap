# django imports
from django.conf import settings
from django.core.cache import cache
from django.template import Library, Node, TemplateSyntaxError
from django.utils.translation import ugettext as _

# portlets imports
import portlets.utils
from portlets.models import Slot

# lfs imports
import lfs.core.utils

register = Library()

class SlotsInformationNode(Node):
    """
    """
    def render(self, context):
        request = context.get("request")
        object = context.get("category") or context.get("product") or context.get("page")
        if object is None:
            object = lfs.core.utils.get_default_shop(request)

        slots = cache.get("slots")
        if slots is None:
            slots = Slot.objects.all()
            cache.set("slots", slots)

        for slot in slots:
            cache_key = "has-portlets-%s-%s-%s" % (object.__class__.__name__, object.id, slot.name)
            has_portlets = cache.get(cache_key)
            if has_portlets is None:
                has_portlets = portlets.utils.has_portlets(object, slot)
                cache.set(cache_key, has_portlets)

            context["Slot%s" % slot.name] = has_portlets

        cache_key = "content-class-%s-%s" % (object.__class__.__name__, object.id)
        content_class = cache.get(cache_key)
#        if content_class is None:
#            content_class = "span-24 last"
#            if context.get("SlotLeft", None) and context.get("SlotRight", None):
#                content_class = "span-15 padding-both"
#            elif context.get("SlotLeft", None):
#                content_class = "span-19 padding-left last"
#            elif context.get("SlotRight", None):
#                content_class = "span-20 padding-right"
#
#            cache.set(cache_key, content_class)

        context["content_class"] = content_class
        return ''

def do_slots_information(parser, token):
    """Calculates some context variables based on displayed slots.
    """
    bits = token.contents.split()
    len_bits = len(bits)
    if len_bits != 1:
        raise TemplateSyntaxError(_('%s tag needs no argument') % bits[0])

    return SlotsInformationNode()

register.tag('slots_information', do_slots_information)


@register.inclusion_tag('lfs/mail/mail_html_footer.html', takes_context=True)
def email_html_footer(context):
    request = context.get('request', None)
    shop = lfs.core.utils.get_default_shop(request)
    return {
        "shop": shop
    }


@register.inclusion_tag('lfs/mail/mail_text_footer.html', takes_context=True)
def email_text_footer(context):
    request = context.get('request', None)
    shop = lfs.core.utils.get_default_shop(request)
    return {
        "shop": shop
    }


@register.filter
def span_for_product_category(value):
    if value == 1:
        return "span12"
    elif value == 2:
        return "span6"
    elif value == 3:
        return "span4"
    elif value == 4:
        return "span3"
    elif value == 6:
        return "span2"
    else:
        raise TemplateSyntaxError(_('%s Product cols are not allowed in preferences. Valid values for Product cols are 1, 2, 3, 4 and 6.') % value)


@register.assignment_tag(takes_context=True)
def categories_for_header(context):
    request = context.get("request")

    product = context.get("product")
    category = context.get("category")
    object = category or product

    if object is None:
        object_id = None
    else:
        object_id = object.id

    cache_key = "%s-categories-header-%s-%s" % (settings.CACHE_MIDDLEWARE_KEY_PREFIX, object.__class__.__name__, object_id)
    result = cache.get(cache_key)
    if result is not None:
        return result

    current_categories = lfs.core.utils.get_current_categories(request, object)

    ct = lfs.core.utils.CategoryTree(current_categories, 1, 4)
    result = ct.get_category_tree()

    cache.set(cache_key, result)
    return result


@register.inclusion_tag('lfs/catalog/category_children.html', takes_context=True)
def sub_categories_for_header(context, categories, level=0):
    level += 1
    result = {"categories": categories, "level": level, "paddingleft": level * 10 + 20}
    return result


@register.assignment_tag(takes_context=True)
def cart_for_header(context):
    import lfs.cart.utils
    request = context.get("request")

    cart = lfs.cart.utils.get_cart(request)
    if cart is None:
        amount_of_items_locale = None
    else:
        amount_of_items_locale = int(cart.get_amount_of_items())

    return amount_of_items_locale

@register.assignment_tag
def mark_search_query(product_name, q):
    l = len(q)
    l_q = q.lower()
    l_product_name = product_name.lower()
    result = product_name

    idx = l_product_name.rfind(l_q)
    while idx > -1:
        result = result[:idx+l] + "</strong>" + result[idx+l:]
        result = result[:idx] + "<strong>" + result[idx:]
        idx = l_product_name.rfind(l_q,0,idx)

    return result
