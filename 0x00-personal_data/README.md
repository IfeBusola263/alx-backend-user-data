## Personal data
I demonstatate:
* How to implement a log filter that will obfuscate PII fields.
* How to encrypt a password and check the validity of an input password.
* How to authenticate to a database using environment variables.

* filtered_logger.py
```
> a function called filter_datum that returns the log message obfuscated.
> Implements the format method to filter values in incoming log records using
filter_datum. Values for fields in fields are filtered.
> Implement a get_logger function that takes no arguments and returns a
logging.Logger object.
> connects to a secure database to read a users table.
> Implement a hash_password function that expects one string argument name
password and returns a salted, hashed password, which is a byte string.
> Implement an is_valid function that expects 2 arguments and returns a boolean.
```