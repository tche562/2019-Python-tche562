import urllib.request
import json
import base64
import nacl.signing
import nacl.encoding
import sqlite3
import time 
import binascii

def veri_broadcast(json_object):

    raw_sig = json_object['signature']
    
    log_rec = json_object['loginserver_record']
    message = json_object['message']
    ts = json_object['sender_created_at']

    # process the information getting from json
    orig_sig = log_rec+message+ts
    byte_orig_sig = bytes(orig_sig,encoding = 'utf-8')
    hex_orig_sig = binascii.b2a_hex(byte_orig_sig)
    byte_raw_sig = bytes(raw_sig,encoding = 'utf-8')

    recordpart = log_rec.split(',')
    byte_pubkey = bytes(recordpart[1],encoding = 'utf-8')

    # generate the verify_key by using the public key of message sender
    verify_key = nacl.signing.VerifyKey(byte_pubkey,
            encoder=nacl.encoding.HexEncoder)

    try:
        verify_key.verify(hex_orig_sig,byte_raw_sig,encoder=nacl.encoding.HexEncoder)
        print('verified---------------------')
    except:
        print('-------------error in verification')








def veri_privatemessage(json_object):

    raw_sig = json_object['signature']
    
    log_rec = json_object['loginserver_record']
    target_pubkey = json_object['target_pubkey']
    target_username = json_object['target_username']
    encrypted_message = json_object['encrypted_message']
    ts = json_object['sender_created_at']

    # process the information getting from json
    orig_sig = log_rec+target_pubkey+target_username+encrypted_message+ts
    byte_orig_sig = bytes(orig_sig,encoding = 'utf-8')
    hex_orig_sig = binascii.b2a_hex(byte_orig_sig)
    byte_raw_sig = bytes(raw_sig,encoding = 'utf-8')

    # turn the target_pubkey from str to byte
    recordpart = log_rec.split(',')
    sender = recordpart[0]
    byte_pubkey = bytes(recordpart[1],encoding = 'utf-8')
    
    # generate the verify_key by using the public key of message sender
    verify_key = nacl.signing.VerifyKey(byte_pubkey,
            encoder=nacl.encoding.HexEncoder)

    try:
        verify_key.verify(hex_orig_sig,byte_raw_sig,encoder=nacl.encoding.HexEncoder)
        print('verified---------------------')
        return sender
    except:
        print('-------------error in verification')






    

