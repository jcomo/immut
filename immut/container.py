"""
example usage:

RequestModel = ImmutableContainer('signature', 'user_id')

u = User('jonathan')
rm = RequestModel('test_signature', u)
print rm.signature  # prints 'test_signature'
rm.signature = 'another_signature'  # raises AttributeError
print rm.password  # raises AttributeError

ResponseModel = ImmutableContainer('message', 'code', builder=True)
builder = ResponseModel()
response = builder.message('hi').status(200).build()

print response.message  # prints 'hi'
response.message = 'hey'  # raises AttributeError


"""