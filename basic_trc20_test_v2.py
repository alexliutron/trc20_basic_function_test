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
owner_address_privateKey = "


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
                              #比如查询TM2TmqauSEiRf16CyFgzHV2BVxBejY9iyR 的余额
                              
                              "parameter":"0000000000000000000000417946F66D0FC67924DA0AC9936183AB3B07C81126", 
                              #地址TM2TmqauSEiRf16CyFgzHV2BVxBejY9iyR 转HexString为：417946F66D0FC67924DA0AC9936183AB3B07C81126
                              #parameter每个参数长度需64位，不足前面补0，故为：0000000000000000000000417946F66D0FC67924DA0AC9936183AB3B07C81126。
                              
                              "fee_limit":1000000000,
                              "call_value":0,
                              "owner_address": owner_address},
                  
        "transfer(address,uint256)":{"contract_address": contractAddress,
                              "function_selector":"transfer(address,uint256)", 
                              #给地址TV3nb5HYFe2xBEmyb3ETe93UGkjAhWyzrs(HexString格式：41D148171F1CEEEB40D668C47D70E7E94E67977559)转账0.00005 trc20_token。(假如trc20_token精度为6，故带精度转账金额为50)
                             
                              "parameter":"000000000000000000000041D148171F1CEEEB40D668C47D70E7E94E679775590000000000000000000000000000000000000000000000000000000000000032",
                              #前64位是address参数：000000000000000000000041D148171F1CEEEB40D668C47D70E7E94E6797755
                              #后64位地址为带精度转账金额的十六进制格式，带精度转账金额50转十六进制后为32，不足64位，前面补0，故为：0000000000000000000000000000000000000000000000000000000000000032
                              
                              "fee_limit":1000000000,
                              "call_value":0,
                              "owner_address": owner_address},
                 
        "approve(address,uint256)":{"contract_address": contractAddress,
                              "function_selector":"approve(address,uint256)",  
                              #账户A允许B账户随意调用不超过A拥有的trc20_token数量,比如A允许B账户调用其100个trc20_token,则账户A需调用approve(B,100)。
                              #账户B：TM2TmqauSEiRf16CyFgzHV2BVxBejY9iyR（41D148171F1CEEEB40D668C47D70E7E94E67977559）
                                    
                              "parameter":"000000000000000000000041D148171F1CEEEB40D668C47D70E7E94E679775590000000000000000000000000000000000000000000000000000000000000064",
                              #前64位为账户B地址转HexString并补0：000000000000000000000041D148171F1CEEEB40D668C47D70E7E94E67977559
                              #后64位为允许B账户随意调用100个(带精度)，转账金额100转16进制为64，并补0:0000000000000000000000000000000000000000000000000000000000000064
                                    
                              "fee_limit":1000000000,
                              "call_value":0,
                              "owner_address": owner_address},
                
        "allowance(address,address)":{"contract_address": contractAddress,
                              "function_selector":"allowance(address,address)", 
                              #allowance(A, B)可以查看B账户还能够调用A账户多少个token
                              
                              "parameter":"0000000000000000000000417946F66D0FC67924DA0AC9936183AB3B07C81126000000000000000000000041D148171F1CEEEB40D668C47D70E7E94E67977559",
                              #前64位为账户A地址转HexString并补0：TM2TmqauSEiRf16CyFgzHV2BVxBejY9iyR（417946F66D0FC67924DA0AC9936183AB3B07C81126）
                              #后64位位账户B地址转HexString并补0：TV3nb5HYFe2xBEmyb3ETe93UGkjAhWyzrs（41D148171F1CEEEB40D668C47D70E7E94E67977559）
                                      
                              "fee_limit":1000000000,
                              "function_selector":"allowance(address,address)", 
                              "function_selector":"allowance(address,address)", 
                              "call_value":0,
                              "owner_address": owner_address}, 
                  
        "transferFrom(address,address,uint256)":{"contract_address": contractAddress,
                              "function_selector":"transferFrom(address,address,uint256)", 
                              #A调用approve(B,100)后，当B账户想用这100个trc20_token中的50个给C账户时，则需B调用transferFrom(A, C, 50)。
                                                 
                              "parameter":"0000000000000000000000417946F66D0FC67924DA0AC9936183AB3B07C81126000000000000000000000041EE06EDC05F8E502A2752FE19FDD83E6DF3AFC8FB0000000000000000000000000000000000000000000000000000000000000032",
                              #有三个参数，每个参数长度64位
                              #前64位为账户A地址转HexString并补0：TM2TmqauSEiRf16CyFgzHV2BVxBejY9iyR（417946F66D0FC67924DA0AC9936183AB3B07C81126）
                              #中间64位为账户C地址转HexString并补0：TXfn88Wcr2fJocZ1dAzxL46xx1jKgpF4f4（41EE06EDC05F8E502A2752FE19FDD83E6DF3AFC8FB）
                              #后64位地址为带精度转账金额的十六进制格式，带精度转账金额50转十六进制后为32，不足64位，前面补0，
                                                 
                              "fee_limit":1000000000,
                              "call_value":0,
                              "owner_address": owner_address_transfrom
                              #此处owner_address为账户B地址
                             }
        
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




