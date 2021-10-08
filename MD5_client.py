import  hashlib

has_code = "17e62166fc8586dfa4d1bc0e1742c08b"





for i in range(1000):
    md5_hash = hashlib.md5()
    md5_hash.update(str(i).encode())
    digest = md5_hash.hexdigest()
    print(i)
    print(digest)
    if(digest==has_code):
        print("niceee")
        print("the number is " + str(i))
        break






