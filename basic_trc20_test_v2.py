#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 11:44:20 2019

@author: alexliu

"""

import requests



#choose the network

network = "shasta"   #main or shasta
#network = "main" 


if network == "main":
    trans_url = "https://api.trongrid.io/wallet/triggersmartcontract"
    sign_url = "https://api.trongrid.io/wallet/gettransactionsign"
    broast_url = "https://api.trongrid.io/wallet/broadcasttransaction"
    ack_trans_url =  "https://api.trongrid.io/wallet/gettransactioninfobyid?value="
else:
    trans_url = "https://api.shasta.trongrid.io/wallet/triggersmartcontract"
    sign_url = "https://api.shasta.trongrid.io/wallet/gettransactionsign"
    broast_url = "https://api.shasta.trongrid.io/wallet/broadcasttransaction"
    ack_trans_url =  "https://api.shasta.trongrid.io/wallet/gettransactioninfobyid?value="
    
    
    
#contract_address
contractAddress = "41a5c20f94c36cdd04165081828a865e028f4fbb25"


#owneraddress&privatekey
owner_address = ""
owner_address_privateKey = ""


# owner_address for test transferFrom
owner_address_transfrom = ""
owner_address_transfrom_privateKey = ""

#trc20 TRC20Interface functions
function_para = {
        "totalSupply()":{"contract_address": contractAddress,
                              "function_selector":"totalSupply()",  
                              "parameter":"",
                              "fee_limit":1000000000,
                              "call_value":0,
                              "owner_address": owner_address},
        
        "balanceOf(address)":{"contract_address": contractAddress,
                              "function_selector":"balanceOf(address)",  
                              "parameter":"0000000000000000000000417946F66D0FC67924DA0AC9936183AB3B07C81126",
                              "fee_limit":1000000000,
                              "call_value":0,
                              "owner_address": owner_address},
                  
        "transfer(address,uint256)":{"contract_address": contractAddress,
                              "function_selector":"transfer(address,uint256)",  
                              "parameter":"000000000000000000000041D148171F1CEEEB40D668C47D70E7E94E679775590000000000000000000000000000000000000000000000000000000000000032",
                              "fee_limit":1000000000,
                              "call_value":0,
                              "owner_address": owner_address},
                 
        "approve(address,uint256)":{"contract_address": contractAddress,
                              "function_selector":"approve(address,uint256)",  
                              "parameter":"000000000000000000000041D148171F1CEEEB40D668C47D70E7E94E679775590000000000000000000000000000000000000000000000000000000000000132",
                              "fee_limit":1000000000,
                              "call_value":0,
                              "owner_address": owner_address},
                
        "allowance(address,address)":{"contract_address": contractAddress,
                              "function_selector":"allowance(address,address)",  
                              "parameter":"0000000000000000000000417946F66D0FC67924DA0AC9936183AB3B07C81126000000000000000000000041D148171F1CEEEB40D668C47D70E7E94E67977559",
                              "fee_limit":1000000000,
                              "call_value":0,
                              "owner_address": owner_address}, 
                  
        "transferFrom(address,address,uint256)":{"contract_address": contractAddress,
                              "function_selector":"transferFrom(address,address,uint256)",  
                              "parameter":"0000000000000000000000417946F66D0FC67924DA0AC9936183AB3B07C81126000000000000000000000041EE06EDC05F8E502A2752FE19FDD83E6DF3AFC8FB0000000000000000000000000000000000000000000000000000000000000032",
                              "fee_limit":1000000000,
                              "call_value":0,
                              "owner_address": owner_address_transfrom}
        
        }



    


for function_name in function_para: 
    print("======================",function_name,"函数===================")
   #print("======================",function_para[function_name],"函数===================")

    #创建交易
    trans_respon = requests.post(trans_url,json=function_para[function_name])
    #交易返回值 + 添加私钥参数
    print("**************trans_respon*************")
    print(trans_respon.json())
            
    if function_name == "totalSupply()" or function_name == "balanceOf(address)" or function_name == "allowance(address,address)" :
        print("**********************"+"Done!"+"***********************") 
    else: 
        #owner_address对应的私钥
        if function_name == "transferFrom(address,address,uint256)":
            sign_private = {"privateKey":owner_address_transfrom_privateKey}
        else:
            sign_private = {"privateKey":owner_address_privateKey}
        trans_respon = dict(trans_respon.json())
        trans_respon.update(sign_private)
        #签名
        sign_respon = requests.post(sign_url,json = trans_respon)    
        #print("**************sign_respon*************")
        #print(sign_respon.json())
        
        #广播
        broast_respon = requests.post(broast_url,json=sign_respon.json())    
        print("**************broast_respon*************")
        print(broast_respon.json())
        
        #确认交易是否成功 
        print("&&&&&&&&&&&&&&&&&&&交易ID&&&&&&&&&&&&&&")
        print(trans_respon["transaction"]["txID"])
        ack_tans_url_end = ack_trans_url + trans_respon["transaction"]["txID"]
        print(ack_tans_url_end)
        ack_trans_respon = requests.get(ack_tans_url_end)
        #print(ack_trans_respon.text)

print("**********************"+"Done!"+"***********************")       




