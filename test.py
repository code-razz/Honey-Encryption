from gen_ai_single import give_decoys
from HE_index import encrypt_message,decrypt_message

# sentences=give_decoys()
# # print("test file")
# print(sentences)

# print(encrypt_message("123","this is test text"))
print(decrypt_message("pass1234",'{"salt": "2QoYA6t7VNHKocF25aeE2A==", "iv": "YyvPNc2hdaMS98be27R4Fw==", "ciphertexts": ["ahYY+7g=", "Vhsd5Pfi77am27GbFoXMvQ7iHW9G26o/lt8S0JVg2Q==", "Vhsd5Pfi77amlayOEITR8NNsb0BlSjqTZI1P2kKRFSbqGCFIn15VJsboVg==", "Vx0G8rvq6POj266fC5LCt1wn29eXIZnW1fFjeuPzesnkwXFq30RRG5fDGdMqQms="]}'))