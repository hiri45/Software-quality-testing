"""
Megamart edits to ensure it passes static tools.

Author - Hirun Hettigoda
"""
from datetime import datetime
from typing import Dict, Tuple, Optional
from DiscountType import DiscountType
from PaymentMethod import PaymentMethod
from FulfilmentType import FulfilmentType
from TransactionLine import TransactionLine
from Transaction import Transaction
from Item import Item
from Customer import Customer
from Discount import Discount

from RestrictedItemException import RestrictedItemException
from PurchaseLimitExceededException import PurchaseLimitExceededException
from InsufficientStockException import InsufficientStockException
from FulfilmentException import FulfilmentException


def is_not_allowed_to_purchase_item(
  item: Item,
  customer: Customer,
  purch_date: str
) -> bool:
    """
    Represent what cannot be purchased.

    Return True if the customer is not allowed to purchase specified item.
    False otherwise. If an item object or the purchase date string was not-
    actually provided, an Exception should be raised.Items that are under
    the alcohol,tobacco or knives category may only be sold to customers who
    are aged 18+ and have their ID verified. An item potentially belongs to
    many categories as long as it belongs to at least one of the three-
    categories above, restrictions apply to that item.The checking of an-
    item's categories against restricted categories should be done in a
    case-insensitive manner.For example, if an item A is in the category
    ['Alcohol'] and item B is in-the category ['ALCOHOL'], both items A and B
    should be identified as restricted items.Even if the customer is aged 18+-
    and is verified, they must provide/link
    their member account to the transaction when purchasing restricted items.
    Otherwise, if a member account is not provided, they will not be allowed -
    to purchase the restricted item even if normally allowed to.
    It is optional for customers to provide their date of birth in their
    profile. Purchase date string should be of the format dd/mm/yyyy.
    The age of the customer is calculated from their specified date of birth,
    which is also of the format dd/mm/yyyy.
    If an item is a restricted item but the purchase or birth date is in the
    incorrect format, an Exception should be raised.
    A customer whose date of birth is 01/08/2005 is only considered to be -
    age 18+ on or after 01/08/2023.
    """
    # Check that an item object and purchase date string are actually provided.
    if item is None:
        raise Exception("Item object must be provided")

    # Check the category/ uppercase category
    restricted_categories = ['alcohol', 'tobacco', 'knives']
    item_categories = [category.lower() for category in item.categories]
    # if the customer buy the restricted category.
    if any(category in restricted_categories for category in item_categories):
        if customer is None:  # No customer link
            return True
        if customer.date_of_birth is None:  # No birthdate
            return True
        if purch_date is None:  # No purchase date
            return True
        if customer.id_verified is False:  # No id verify
            return True

        # Validate the purchase date and birthdate.
        format_date = "%d/%m/%Y"
        purchase_date = ""
        birth_date = ""
        try:
            purchase_date = datetime.strptime(purch_date, format_date)
        except ValueError:
            raise Exception("Incorrect date format")
        try:
            birth_date = datetime.strptime(customer.date_of_birth, format_date)
        except ValueError:
            raise Exception("Incorrect birth date format")

    # compare the purchase date and birhtdate in YEAR, MONTH, DATE
        if round(purchase_date.year - birth_date.year) < 18:
            return True  # Customer is under 18
        if purchase_date.month > birth_date.month:
            return False
        if purchase_date.month < birth_date.month:
            return True
        if purchase_date.day > birth_date.day:
            return False
        if purchase_date.day < birth_date.day:
            return True
    # Non restircted categories
    return False


def get_item_purchase_quantity_limit(
    item: Item,
    items_dict: Dict[str, Tuple[Item, int, Optional[int]]]
) -> Optional[int]:
    """
    Represent the limits of an item.

    For a given item, returns the integer purchase quantity limit.
    If an item object or items dictionary was not actually provided, an-
    Exception should be raised.If the item was not found in the items-
    dictionary-or if the item does not have a purchase quantity limit,-
    None should be returned.The items dictionary (which is a mapping-
    from keys to values) -
    contains string-item IDs as its keys,and tuples containing an item-
    object, integer stock level-and an optional integer purchase quantity-
    limit (which may be None) that correspond- to their respective-
    item ID as values.
    """
    if item is None:
        raise Exception("There is no item")
    if items_dict is None:
        raise Exception()
    # Check if the item exists in the dictionary
    if item.id not in items_dict:
        return None

    # Extract the tuple from the dictionary
    item_tuple = items_dict[item.id]

    # Extract the purchase quantity limit from the tuple
    _, _, purchase_limit = item_tuple
    return purchase_limit


def is_item_sufficiently_stocked(
    item: Item,
    purchase_quantity: int,
    items_dict: Dict[str, Tuple[Item, int, Optional[int]]]
) -> bool:
    """
    Represent the right stock information for item.

    For a given item, returns True if the purchase quantity does not.
    exceed the currently available stock, or False if it exceeds, or
    the item was not found in the items dictionary.If an item object,
    purchase quantity or items dictionary was not actually provided,
    an Exception should be raised.Purchase quantity should be
    minimum of 1, and stock level is always a minimum of 0.
    Otherwise, an Exception should be raised for each of these
    situations.The items dictionary (which is a mapping from keys to
    values) contains string item IDs as its keys,and tuples containing
    an item object, integer stock level and an optional integer purchase
    quantity limit (which may be None) that correspond to their respective
    item ID as values.
    """
    if item is None:
        raise Exception("Item object must be provided")
    if purchase_quantity is None:
        raise Exception("Not find purchase quantity")
    if items_dict is None:
        raise Exception("Not find dict")
    if item.id not in items_dict:
        return False
    _, stock_level, optional_purchase_quantity = items_dict[item.id]
    if purchase_quantity < 1:
        raise Exception("Purchase quantity must be at least 1")
    if stock_level < 0:
        raise Exception("Stock level cannot be negative")
    if purchase_quantity <= stock_level:
        return True
    if purchase_quantity > stock_level:
        return False


def calculate_final_item_price(
    item: Item,
    discounts_dict: Dict[str, Discount]
) -> float:
    """
    Represent the final price.

    Item's final price may change if there is currently a discount.
    If an item object or discounts dictionary was not
    actually provided, an Exception should be raised.There are two types
    of discounts - it may be a percentage off the original price, or a
    flat amount off the original price.Percentage-based discounts have a
    value defined between 1 and 100 inclusive. Otherwise, an Exception
    should be thrown.For example, a percentage-type discount of value 25
    means a 25% discount should be applied to that item.Flat-based discounts
    should not cause the item's final price to be more than its original
    price or be negative. Otherwise, an Exception should be thrown.For
    example, a flat-type discount of value 1.25 means a discount of $1.25
    should be applied to that item.The discounts dictionary (which is a
    mapping from keys to values) contains string item IDs as its keys, and
    discount objects that correspond to their respective item ID as values.
    If an item has an associated discount, the discounts dictionary (which is
    a mapping from keys to values) will contain a key corresponding to the
    ID of that item.
    Otherwise, if the item does not have an associated discount, its final
    price would be the same as its original price.
    """
    # Check that an item object, discount dict
    if item is None:
        raise Exception("invalid item")
    if discounts_dict is None:
        raise Exception("Invalid dictionary")

    # Check if the item in the discount dicts
    if item.id not in discounts_dict:
        return round(item.original_price, 2)

    discounts = discounts_dict.get(item.id)
    discount_amount = 0.0

    if discounts.type == DiscountType.PERCENTAGE:  # Percentage
        if not (1 <= discounts.value <= 100):
            raise Exception("Invalid percentage")
        discount_amount = item.original_price * (discounts.value/100)

    elif discounts.type == DiscountType.FLAT:  # Flat
        if discounts.value < 0 or discounts.value > item.original_price:
            raise Exception("Invalid flat discount value")
        discount_amount = discounts.value

    final = item.original_price - discount_amount
    return round(final, 2)


def calculate_item_savings(
    item_original_price: float,
    item_final_price: float
) -> float:
    """
    Represent the savings made.

    Saves on an item is defined as how much money you would not need to.
    spend on an item compared to if you bought it at its original price.
    If an item's original price or final price was not actually provided,
    an Exception should be raised.If the final price of the item is greater
    than its original price, an Exception should be raised.
    """
    if item_original_price is None:
        raise Exception("Original price not provided")
    if item_final_price is None:
        raise Exception("Final price not provided")

    if item_final_price > item_original_price:
        raise Exception("Final price cannot be greater than original price")

    saving = item_original_price - item_final_price
    return round(saving, 2)


def calculate_fulfilment_surcharge(
    fulfilment_type: FulfilmentType,
    customer: Customer
) -> float:
    """
    Represent the surcharge based on fulfilment type.

    A fulfilment surcharge is only applicable for deliveries.
    Is no surcharge applied in any other case.The fulfilment surcharge is
    calculated as $5 or $0.50 for every kilometre, whichever is greater.
    Surcharge value returned should have at most two decimal places.
    If a fulfilment type was not actually provided, an Exception should be
    raised.Delivery fulfilment type can only be used if the customer has linked
    their member account to the transaction, and if delivery distance is
    specified in their member profile.Otherwise, a FulfilmentException should
    be raised.
    """
    # Exceptions
    if fulfilment_type is None:
        raise Exception("The fullfilment_type are not provided")
    # Choose anything other than delivery then return 0
    if fulfilment_type != FulfilmentType.DELIVERY:
        return 0.00
    if customer is None:
        raise FulfilmentException("The customer delivery are not provided")
    if customer.delivery_distance_km is None:
        raise FulfilmentException("The delivery distance are not provided")
    # if the amount less equal than the 5.0
    if round(customer.delivery_distance_km*0.5, 2) <= 5.0:
        return 5.00  # then return 5
    # otherwise times that by 0.5
    return round(customer.delivery_distance_km*0.5, 2)


def round_off_subtotal(
    subtotal: float,
    payment_method: PaymentMethod
) -> float:
    """
    Represent the rounding of the subtotal.

    Subtotal rounding is only applicable when paying by cash.
    There is no rounding performed in any other case.
    If the subtotal value or payment method was not actually provided, an
    Exception should be raised.The subtotal is rounded off to the nearest
    multiple of 5 cents. Surcharge value returned should have at most two
    decimal places.Cent amounts which have their ones-place digit as 1 - 2
    or 6 - 7 will be rounded down. If it is 3 - 4 or 8 - 9, it will be
    rounded up instead.As the (monetary) subtotal value is provided as a float,
    ensure that it is first rounded off to two decimal places before doing the
    rounding.
    """
    # Raise Exception for these conditions
    subtotal = round(subtotal, 2)
    # if type(subtotal) != float:
    # raise Exception("Missing subtotal")
    if not isinstance(payment_method, PaymentMethod):
        raise Exception("Missing Payment method")

    if payment_method.value == PaymentMethod.CASH.value:
        num = int((subtotal*1000)/10)
        if (num - 1) % 10 == 0 or (num - 6) % 10 == 0:
            return round(subtotal - 0.01, 2)
        elif (num - 2) % 10 == 0 or (num - 7) % 10 == 0:
            return round(subtotal - 0.02, 2)
        elif (num - 4) % 10 == 0 or (num - 9) % 10 == 0:
            return round(subtotal + 0.01, 2)
        elif (num - 3) % 10 == 0 or (num - 8) % 10 == 0:
            return round(subtotal + 0.02, 2)

    return subtotal


def checkout(
  transaction: Transaction,
  items_dict: Dict[str, Tuple[Item, int, Optional[int]]],
  discounts_dict: Dict[str, Discount]
) -> Transaction:
    """
    Represent the final checkout using all methods.

    Method will need to utilise all of the seven methods above.
    As part of the checkout process, each of the transaction lines in the
    transaction should be processed.If a transaction object, items
    dictionary or discounts dictionary was not actually provided, an
    Exception should be raised.All items in the transaction should be
    checked against any restrictions, available stock levels and purchase
    quantity limits.If a restricted item in the transaction may not be
    purchased by the customer initiating the transaction, a
    RestrictedItemException should be raised.If an item in the transaction
    exceeds purchase quantity limits, a PurchaseLimitExceededException should
    be raised.If an item in the transaction is of insufficient stock, an
    InsufficientStockException should be raised.All of the transaction lines
    will need to be processed in order to calculate its respective final price
    after applicable discounts have been applied.The subtotal, surcharge and
    rounding amounts, as well as final total, total savings from discounts and
    total number of items purchased also need to be calculated for the
    transaction.Once the calculations are completed, the updated transaction
    object should be returned.
    """
    # Validate The transaction and items_dict, discounts_dict
    if transaction is None:
        raise Exception("Missing Transaction")
    if items_dict is None:
        raise Exception("Missing items_dict")
    if discounts_dict is None:
        raise Exception("Missing discount_dict")
    # Initialize the variables
    transaction.amount_saved = 0.0
    transaction.total_items_purchased = 0
    transaction.all_items_subtotal = 0.0
    transaction.fulfilment_surcharge_amount = 0.0
    transaction.rounding_amount_applied = 0.0
    transaction.final_total = 0.0
    counter = {}
    # loop through items in the trans line
    for line in transaction.transaction_lines:
        if line.item.id in counter:
            counter[line.item.id] += line.quantity
        else:
            counter[line.item.id] = line.quantity

    # Raise any Exception if happens
        if is_not_allowed_to_purchase_item(
          line.item,
          transaction.customer,
          transaction.date):
            raise RestrictedItemException("Can not buy")
        if not is_item_sufficiently_stocked(
          line.item,
          counter[line.item.id],
          items_dict) or not is_item_sufficiently_stocked(
          line.item,
          line.quantity,
          items_dict):
            raise InsufficientStockException("Over stocked")
        if get_item_purchase_quantity_limit(line.item, items_dict) is not None:
            if get_item_purchase_quantity_limit(
              line.item,
              items_dict) < counter[
              line.item.id] or get_item_purchase_quantity_limit(
              line.item,
              items_dict
              ) < line.quantity:
                raise PurchaseLimitExceededException("Exceeded quantity")

        transaction.total_items_purchased += line.quantity
        # The total of the final items cost after discount
        line.final_cost = calculate_final_item_price(
          line.item,
          discounts_dict) * line.quantity
        transaction.all_items_subtotal += line.final_cost

        # Save the toal
        transaction.amount_saved += calculate_item_savings(
          line.item.original_price,
          calculate_final_item_price(
            line.item,
            discounts_dict)) * line.quantity

    # set the subtotal, savings surcharge,
    # rounding amount, final total in the transaction object,
    transaction.fulfilment_surcharge_amount = calculate_fulfilment_surcharge(
      transaction.fulfilment_type,
      transaction.customer)
    transaction.rounding_amount_applied = round(round_off_subtotal(
      transaction.all_items_subtotal,
      transaction.payment_method) - transaction.all_items_subtotal, 2)
    sub = transaction.all_items_subtotal
    rounded = transaction.rounding_amount_applied
    surch = transaction.fulfilment_surcharge_amount
    transaction.final_total = sub + rounded + surch
    TransactionLine

    return transaction
