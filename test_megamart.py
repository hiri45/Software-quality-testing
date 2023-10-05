import unittest
import megamart
from FulfilmentException import FulfilmentException
from FulfilmentType import FulfilmentType

from RestrictedItemException import RestrictedItemException
from PurchaseLimitExceededException import PurchaseLimitExceededException
from InsufficientStockException import InsufficientStockException
from FulfilmentException import FulfilmentException
from InsufficientFundsException import InsufficientFundsException


class TestMegaMart(unittest.TestCase):
  def test_is_not_allowed_to_purchase_item(self):
    item_alcohol = megamart.Item('1', 'Wine', 10.0, ['Alcohol'])
    item_alcohol_uppercase = megamart.Item('1', 'Wine', 10.0, ['ALCOHOL'])
    item_tobacco = megamart.Item('2', 'Cigarettes', 5.0, ['Tobacco'])
    item_knives = megamart.Item('3', 'Kitchen Knife', 15.0, ['Knives'])
    item_confectionery = megamart.Item('4', 'Chocolate Bar', 2.0, ['Confectionery'])
    customer_underage = megamart.Customer('001', 'Bob', '01/08/2010', True, 5.0)
    customer_adult = megamart.Customer('002', 'Alice', '01/08/1990', True, 10.0)
    customer_adult_no_member = megamart.Customer('003', 'Alice', '01/08/1990', False, 8.0)
    customer_no_date = megamart.Customer('004', 'Alpha', None, True, 10.0)
    customer_missID_birthdate = megamart.Customer('001', 'Charlie',None, False, 10.0)
    customer_wrong_format_date = megamart.Customer('002', 'Charlie', '01-08-1990', True, 10.0)
    wrong_format_purchase_date = '01-08-2023'
    purchase_date = '01/08/2023'
    customer_18 = megamart.Customer('001', 'Bob', '01/08/2005', True, 5.0)
    customer_notMonth = megamart.Customer('001', 'Bob', '01/09/2005', True, 5.0)
    customer_theMonth = megamart.Customer('001', 'Bob', '01/07/2005', True, 5.0)
    purchase_date2 = '05/08/2023'
    customer_notDate = megamart.Customer('001', 'Charlie', '07/08/2005', True, 5.0)
    customer_theDate = megamart.Customer('001', 'Charlie', '04/08/2005', True, 5.0)
    with self.assertRaises(Exception):
      megamart.is_not_allowed_to_purchase_item(item_alcohol, customer_underage,wrong_format_purchase_date)
    with self.assertRaises(Exception):
      megamart.is_not_allowed_to_purchase_item(item_alcohol, customer_wrong_format_date, purchase_date)
    with self.assertRaises(Exception):
      megamart.is_not_allowed_to_purchase_item(None, customer_underage, purchase_date)
    #Check with restricted item if no connected account, no birthdate, no link members when buying the restricted item
    self.assertTrue(megamart.is_not_allowed_to_purchase_item(item_alcohol,None, purchase_date))
    self.assertTrue(megamart.is_not_allowed_to_purchase_item(item_alcohol,customer_no_date, purchase_date))
    self.assertTrue(megamart.is_not_allowed_to_purchase_item(item_alcohol,customer_adult_no_member, purchase_date))
    self.assertTrue(megamart.is_not_allowed_to_purchase_item(item_tobacco,customer_underage, purchase_date))
    self.assertTrue(megamart.is_not_allowed_to_purchase_item(item_knives,customer_underage, purchase_date))
    self.assertFalse(megamart.is_not_allowed_to_purchase_item(item_alcohol,customer_adult, purchase_date))
    self.assertFalse(megamart.is_not_allowed_to_purchase_item(item_tobacco,customer_adult, purchase_date))
    self.assertFalse(megamart.is_not_allowed_to_purchase_item(item_knives,customer_adult, purchase_date))
    self.assertTrue(megamart.is_not_allowed_to_purchase_item(item_alcohol,customer_adult_no_member, purchase_date))
    self.assertTrue(megamart.is_not_allowed_to_purchase_item(item_tobacco,customer_adult_no_member, purchase_date))
    self.assertTrue(megamart.is_not_allowed_to_purchase_item(item_knives,customer_adult_no_member, purchase_date))
    #Check month adn date:
    self.assertFalse(megamart.is_not_allowed_to_purchase_item(item_alcohol,customer_theDate, purchase_date2))
    self.assertFalse(megamart.is_not_allowed_to_purchase_item(item_tobacco,customer_theMonth, purchase_date))
    #Check years
    self.assertTrue(megamart.is_not_allowed_to_purchase_item(item_alcohol,customer_notDate, purchase_date2))
    self.assertTrue(megamart.is_not_allowed_to_purchase_item(item_tobacco,customer_notMonth, purchase_date)) 
    # Raise any Exception if happens
    #check with the non restricted item
    self.assertFalse(megamart.is_not_allowed_to_purchase_item(item_confectionery,customer_underage, purchase_date))
    self.assertFalse(megamart.is_not_allowed_to_purchase_item(item_confectionery,customer_adult, purchase_date))
    self.assertFalse(megamart.is_not_allowed_to_purchase_item(item_confectionery,customer_adult_no_member, purchase_date))
    #check with the non restricted item when birthdate provdied, purchae date in wrong format
    self.assertFalse(megamart.is_not_allowed_to_purchase_item(item_confectionery,customer_underage, wrong_format_purchase_date))
    self.assertFalse(megamart.is_not_allowed_to_purchase_item(item_confectionery,customer_wrong_format_date, purchase_date))
    #Return True if no provided purchase date
    self.assertTrue(megamart.is_not_allowed_to_purchase_item(item_alcohol,customer_adult,None))
    self.assertTrue(megamart.is_not_allowed_to_purchase_item(item_alcohol,customer_underage,None))
    #Return False if customer the same day and years
    self.assertFalse(megamart.is_not_allowed_to_purchase_item(item_alcohol,customer_18,purchase_date))
  
  def test_get_item_purchase_quantity_limit(self):
    #Raise exception if happens
    with self.assertRaises(Exception):
      megamart.get_item_purchase_quantity_limit(None, "2")
    with self.assertRaises(Exception):
      megamart.get_item_purchase_quantity_limit("1", None)
    with self.assertRaises(Exception):
      megamart.get_item_purchase_quantity_limit(None, None)
    # Tuple format: (Item, Current Stock Level, Purchase Quantity Limit)
    # Define Items and items dict
    item_alcohol = megamart.Item('1', 'Wine', 10.0, ['Alcohol'])
    item_tobacco = megamart.Item('2', 'Cigarettes', 5.0, ['Tobacco'])
    item_knives = megamart.Item('3', 'Kitchen Knife', 15.0, ['Knives'])
    items_dict = {
      "1": (item_alcohol, 30, None),
      "2": (item_tobacco, 50, 5),
    } 
    #Return None
    self.assertIsNone(megamart.get_item_purchase_quantity_limit(item_alcohol, items_dict))
    self.assertIsNone(megamart.get_item_purchase_quantity_limit(item_knives, items_dict))
    self.assertEqual(megamart.get_item_purchase_quantity_limit(item_tobacco, items_dict),5)
  def test_is_item_sufficiently_stocked(self):
    # Define the variable
    items_dict = {
      "1": (megamart.Item("1", "Wine", 10.0, ["Alcohol"]), 5, 10),
      "2": (megamart.Item("2", "Cigarettes", 20.0, ["Tobacco"]), 0, None),
      "3": (megamart.Item("3", "Gin", 15.0, ["ALCOHOL"]), -1, None),
      "4": (megamart.Item("4", "TimTam", 10.0, ["Confectionery"]), 5, 10)
    }
    item1 = megamart.Item("1", "Wine", 10.0, ["Alcohol"])
    item2 = megamart.Item("2", "Cigarettes", 20.0, ["Tobacco"])
    item3 = megamart.Item("3", "Gin", 15.0, ["ALCOHOL"])
    item5 = megamart.Item("5", "Item 5", 20.0, ["category5"])
    #Raise any exception if happens
    with self.assertRaises(Exception):
      megamart.is_item_sufficiently_stocked(None,1,items_dict)
    with self.assertRaises(Exception):
      megamart.is_item_sufficiently_stocked(item1, None, items_dict)
    with self.assertRaises(Exception):
      megamart.is_item_sufficiently_stocked(item2, 1, None)
    with self.assertRaises(Exception):
      megamart.is_item_sufficiently_stocked(item1, 0, items_dict)
    with self.assertRaises(Exception):
      megamart.is_item_sufficiently_stocked(item3,10, items_dict)
    self.assertFalse(megamart.is_item_sufficiently_stocked(item5, 11, items_dict))

  def test_calculate_final_item_price(self):
    discounts_dict = {
      "2": megamart.Discount(megamart.DiscountType.PERCENTAGE, 25, "Cigarettes"),
      "3": megamart.Discount(megamart.DiscountType.FLAT, 20, "Gin"),
      "4": megamart.Discount(megamart.DiscountType.PERCENTAGE, 120, "item4"),
      "5": megamart.Discount(megamart.DiscountType.FLAT, 190, "item5"),
      "6": megamart.Discount("InvalidType", 10, "item6"),
    }
    items_dict = {
      "1": megamart.Item("1", "Wine", 110.0, ["Alcohol"]),
      "2": megamart.Item("2", "Cigarettes", 300.0, ["Tobacco"]),
      "3": megamart.Item("3", "Gin", 140.0, ["ALCOHOL"]),
      "4": megamart.Item("4", "TimTam",  50.0, ["Confectionery"]),
      "5": megamart.Item("5", "Item 5", 80.0, ["category5"]),
      "6": megamart.Item("6", "Item 6", 60.0, ["category6"]),
      "7": megamart.Item("7", "Item 7", 70.0, ["category7"]),

    }
    # Check the discount return 
    self.assertEqual(megamart.calculate_final_item_price(items_dict["7"], discounts_dict), 70.0)
    self.assertEqual(megamart.calculate_final_item_price(items_dict["2"], discounts_dict), 225.0)
    self.assertEqual(megamart.calculate_final_item_price(items_dict["3"], discounts_dict), 120.0)

    # Raise any exception if happens
    with self.assertRaises(Exception):
      megamart.calculate_final_item_price(None, discounts_dict)
    with self.assertRaises(Exception):
      megamart.calculate_final_item_price(items_dict["5"],None)
    with self.assertRaises(Exception):
      megamart.calculate_final_item_price(items_dict["4"],discounts_dict)
    with self.assertRaises(Exception):
      megamart.calculate_final_item_price(items_dict["5"],discounts_dict)
  
  def test_calculate_item_savings(self):
    #Valid savings calculation
    item_original_price = 100.0
    item_final_price = 80.0
    savings = megamart.calculate_item_savings(item_original_price, item_final_price)
    self.assertEqual(savings, 20.0, "Incorrect savings calculation")

    # Test case: Original price not provided
    with self.assertRaises(Exception, msg="Exception raised for missing original price"):
      megamart.calculate_item_savings(None, item_final_price)

        # Test case: Final price not provided
    with self.assertRaises(Exception, msg="Final price not provided"):
      megamart.calculate_item_savings(item_original_price, None)

        # Test case: Final price greater than original price
    item_original_price = 100.0
    item_final_price = 120.0
    with self.assertRaises(Exception, msg="Exception not raised for final price greater than original price"):
      megamart.calculate_item_savings(item_original_price, item_final_price)
   
  def test_calculate_fulfilment_surcharge(self):
    with self.assertRaises(Exception, msg="FulfilmentException not raised"):
      megamart.calculate_fulfilment_surcharge(FulfilmentType.DELIVERY, None)
    customer_pickup1 = megamart.Customer("12345", "John Doe", "1990-01-15", True, 8.00)
    fulfilment_type_pickup1 = megamart.FulfilmentType.PICKUP
    surcharge_invalid_pickup = megamart.calculate_fulfilment_surcharge(fulfilment_type_pickup1, customer_pickup1)
    self.assertEqual(surcharge_invalid_pickup,0.00)
#
    customer_no_verification1 = megamart.Customer("12345", "John Doe", "1990-01-15", False, 10.0)
    with self.assertRaises(Exception, msg="FulfilmentException not raised"):
      megamart.calculate_fulfilment_surcharge(None, customer_no_verification1)

#
    customer_no_verification3 = megamart.Customer("12345", "John Doe", "1990-01-15", True, None)
    fulfilment_type_verification2 = megamart.FulfilmentType.DELIVERY
    with self.assertRaises(Exception, msg="FulfilmentException not raised"):
      megamart.calculate_fulfilment_surcharge(fulfilment_type_verification2, customer_no_verification3)
#
    customer_pickup1 = megamart.Customer("12345", "John Doe", "1990-01-15", True, 7)
    fulfilment_type_pickup2 = megamart.FulfilmentType.DELIVERY
    surcharge_valid_pickup1 = megamart.calculate_fulfilment_surcharge(fulfilment_type_pickup2, customer_pickup1)
    self.assertEqual(surcharge_valid_pickup1,5)
###
    customer_pickup2 = megamart.Customer("12345", "John Doe", "1990-01-15", True, 20)
    fulfilment_type_pickup3 = megamart.FulfilmentType.DELIVERY
    surcharge_valid_pickup2 = megamart.calculate_fulfilment_surcharge(fulfilment_type_pickup3, customer_pickup2)
    self.assertEqual(surcharge_valid_pickup2,10)
  
  def test_round_off_subtotal(self):
    #Wrong way to set variable
    CASH = megamart.PaymentMethod.CASH 
    DEBIT = megamart.PaymentMethod.DEBIT
    CREDIT = megamart.PaymentMethod.CREDIT
    # Some example total
    sub_total0 = 19.80
    sub_total5 = 19.85
    sub_total6 = 19.86
    sub_total9 = 19.89
    sub_total10 = 19.90
    sub_total11 = 19.873

    #Check if they are not provided
    with self.assertRaises(Exception):
      megamart.round_off_subtotal(None,DEBIT)
    with self.assertRaises(Exception):
      megamart.round_off_subtotal(None,CASH)
    with self.assertRaises(Exception):
      megamart.round_off_subtotal(None,CREDIT)
    with self.assertRaises(Exception):
      megamart.round_off_subtotal(None,None)
    
    with self.assertRaises(Exception):
      megamart.round_off_subtotal(sub_total0,None)
    #Test other cases that not CASH
    self.assertEqual(megamart.round_off_subtotal(sub_total0,DEBIT),sub_total0)
    self.assertEqual(megamart.round_off_subtotal(sub_total0,CREDIT),sub_total0)
    
    #Test all case with CASH
    self.assertEqual(megamart.round_off_subtotal(sub_total0,CASH),sub_total0)
    self.assertEqual(megamart.round_off_subtotal(sub_total6,CASH),sub_total5)
    self.assertEqual(megamart.round_off_subtotal(sub_total9,CASH),sub_total10)
    self.assertEqual(megamart.round_off_subtotal(sub_total11,CASH),sub_total5)


  def test_checkout(self):
    #Items
    item_tobacco = megamart.Item('1', 'Cigarettes',10.0, ['Tobacco'])
    item_alcohol = megamart.Item('2', 'Wine', 10.0, ['Alcohol'])
    item_knives = megamart.Item('3', 'Kitchen', 12.5,['Knife'])
    item_Timtam = megamart.Item('4', 'Timtam', 10.4,['Confectionery'])
    item_Timtam_chocolate = megamart.Item('5', 'Timtam_chocolate', 10.56,['Confectionery'])
    #Items dictionaries
    
    # Customers
    customer_underage = megamart.Customer('001', 'Bob', '09/07/2015', True, 5.0) # Delviery = 5
    customer_adult = megamart.Customer('002', 'Alice', '01/08/1990', True, 10.0) # Delviery = 5
    customer_adult_no_member = megamart.Customer('003', 'Alice', '01/08/1990', False, 8.0) # Delviery = 5

    #Discount dictionaries
    discounts_dict = {
      "1": megamart.Discount(megamart.DiscountType.PERCENTAGE, 25, "1"), # Discount 25%
      "2": megamart.Discount(megamart.DiscountType.PERCENTAGE, 25, "2"), # Discount 25%
      "3": megamart.Discount(megamart.DiscountType.FLAT, 2, "3"), # Discount = 2
      "4": megamart.Discount(megamart.DiscountType.PERCENTAGE, 15, "4"), # Delviery 15%
      "5": megamart.Discount(megamart.DiscountType.FLAT,2, "5"), # discounts_dict = 2
    }
    items_dict = {
      "1": (item_tobacco, 30, 10), # Tuple format: (Item, Current, Stock Level, Purchase Quantity Limit)
      "2": (item_alcohol,30, 10),
      "3": (item_knives,5,2),
      "4": (item_Timtam,3,5),
      "5": (item_Timtam_chocolate,20,5),
    } 
    
    #Transaction for underage
    transaction1 = megamart.Transaction('01/08/2023', '12:00:00') # Date and times
    transaction1.customer = customer_underage
    transaction1.fulfilment_type = FulfilmentType.PICKUP
    transaction1.payment_method = megamart.PaymentMethod.CASH
    transaction1.transaction_lines = [ 
      megamart.TransactionLine(item_tobacco, 2),
      megamart.TransactionLine(item_alcohol,2),
      megamart.TransactionLine(item_knives,6)
    ]
    #Transaction for adult
    transaction2 = megamart.Transaction('01/08/2023', '12:00:00') # Date and times
    transaction2.customer = customer_adult
    transaction2.fulfilment_type = FulfilmentType.PICKUP
    transaction2.payment_method = megamart.PaymentMethod.CASH
    transaction2.transaction_lines = [ 
      megamart.TransactionLine(item_tobacco, 2),
      megamart.TransactionLine(item_alcohol, 15),
      megamart.TransactionLine(item_knives,6)
    ]

    #Transaction for adult - 2
    transaction3 = megamart.Transaction('01/08/2023', '12:00:00') # Date and times
    transaction3.customer = customer_adult
    transaction3.fulfilment_type = FulfilmentType.PICKUP
    transaction3.payment_method = megamart.PaymentMethod.CASH
    transaction3.transaction_lines = [ 
      megamart.TransactionLine(item_Timtam, 4)
    ]

    transaction4 = megamart.Transaction('01/08/2023', '12:00:00') # Date and times
    transaction4.amount_tendered = 200.00
    transaction4.customer = customer_adult
    transaction4.fulfilment_type = FulfilmentType.PICKUP
    transaction4.payment_method = megamart.PaymentMethod.CASH
    transaction4.transaction_lines = [ 
      megamart.TransactionLine(item_tobacco, 5), # Original = 50
      megamart.TransactionLine(item_alcohol, 5), # Original = 50
      megamart.TransactionLine(item_knives,2), # Original = 25
      megamart.TransactionLine(item_Timtam_chocolate,3) # Original = 31.68
      #Total = 156.68
      #Total Discount = 121.68
    ]

    transaction5 = megamart.Transaction('01/08/2023', '12:00:00') # Date and times
    transaction5.customer = customer_adult
    transaction5.amount_tendered = 200.00
    transaction5.fulfilment_type = FulfilmentType.DELIVERY
    transaction5.payment_method = megamart.PaymentMethod.CREDIT
    transaction5.transaction_lines = [ 
      megamart.TransactionLine(item_tobacco, 5),  # Original = 50
      megamart.TransactionLine(item_alcohol, 5),  # Original = 50
      megamart.TransactionLine(item_knives,2),  # Original = 20
      megamart.TransactionLine(item_Timtam_chocolate,3),
      megamart.TransactionLine(item_Timtam_chocolate,1)  # Original = 30
      #Total = 156.68
      #Total Discount = 121.68
    ]


    items_dict_1 = {
      "1": (item_tobacco, 30, 10), # Tuple format: (Item, Current, Stock Level, Purchase Quantity Limit)
      "2": (item_alcohol,30, 10),
      "3": (item_knives,5,2),
    } 
    #Check raise Exception
    with self.assertRaises(Exception):
      megamart.checkout(None, items_dict_1, discounts_dict)
    with self.assertRaises(Exception):
      megamart.checkout(transaction1, None, discounts_dict)
    with self.assertRaises(Exception):
      megamart.checkout(transaction1,items_dict,None)
    
    with self.assertRaises(RestrictedItemException):
      megamart.checkout(transaction1,items_dict,discounts_dict)
    with self.assertRaises(PurchaseLimitExceededException):
      megamart.checkout(transaction2,items_dict,discounts_dict)
    with self.assertRaises(InsufficientStockException):
      megamart.checkout(transaction3,items_dict,discounts_dict)
    

    test1 = megamart.checkout(transaction4,items_dict,discounts_dict)
    self.assertEqual(test1.fulfilment_surcharge_amount,0.00)
    self.assertEqual(test1.rounding_amount_applied,0.02)
    self.assertEqual(test1.final_total,121.7)
    self.assertEqual(test1.all_items_subtotal,121.68)
    self.assertEqual(test1.total_items_purchased,15)
    self.assertEqual(test1.amount_saved,35.0)
    
    test2 = megamart.checkout(transaction5,items_dict,discounts_dict)
    self.assertEqual(test2.fulfilment_surcharge_amount,5.00)
    
unittest.main()


