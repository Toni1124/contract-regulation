#  Created by Jiashuo Zhang on 2020/12/2.
#  Modified by Jianbo Gao on 2020/12/3
#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import subprocess
from subprocess import PIPE
import json 
from _pysha3 import keccak_256

class Solidity_Storage:
    'Solidity_Storage is used to calculate offset and slot for solidity storage variables'
    sourcecode=''       # Solidity Source Code
    solc_path=''        # Solidity Enviroment Variable, if you add solc into your enviroment, then your solc_path is 'solc'
    solc_output=''      # The compiling result from solc
    origin_location=[]  # origin locations of variables, users donnot need to care about it.
    origin_types={}     # origin types of variables, users donnot need to care about it.
    abis = {}           # ABI of all contracts
    bytecodes = {}      # bytecode of all contracts

    '''
    __init__() trys to compile the sourcecode using solc and parse the result. 
    parameters: sourcecode and solc_path is the same as before. A tmp_folder is required to use solc, you can give an empty folder or use the default path'/tmp'
    '''
    def __init__(self,sourcecode,solc_path):
        self.soucecode=sourcecode
        self.solc_path=solc_path
        pattern={}
        input_json={'language':'Solidity','sources':{'file':{'content':sourcecode}},'settings':{'outputSelection':{'file':{"*":["storageLayout","evm.bytecode.object", "abi"]}}}}
        output_json=''
        args=[self.solc_path,'--standard-json']
        try:
            proc = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            (out, err) = proc.communicate(json.dumps(input_json).encode('utf-8'))
            out = out.decode('utf-8')
            self.solc_output = out
        except :
            # logging.error("Cannot compile the source file")
            raise Exception("Cannot compile the source file")
        try:
            output=json.loads(self.solc_output)
            contract_list=output['contracts']['file'].values()
            for contract_name in output['contracts']['file']:
                self.abis[contract_name] = output['contracts']['file'][contract_name]['abi']
                self.bytecodes[contract_name] = output["contracts"]["file"][contract_name]["evm"]["bytecode"]["object"]
        except:
            # logging.error("Invalid output from solc: %s. Perhaps the compiling fails or your solc needs to update to 0.5.13"%self.solc_output)
            raise Exception("Invalid output from solc: %s. Perhaps the compiling fails or your solc needs to update to 0.5.13"%self.solc_output)
        try:
            for one_dict in contract_list:
                self.origin_location.extend(one_dict['storageLayout']['storage'])
            for one_dict in contract_list:
                if one_dict['storageLayout']['types'] is not None:
                    for key in one_dict['storageLayout']['types'].keys():
                        self.origin_types[key]=one_dict['storageLayout']['types'][key]
        except:
            # logging.error("Invalid output from solc. Your solc needs to update to 0.5.13")
            raise Exception("Invalid output from solc. Your solc needs to update to 0.5.13")
    '''
        __find_item is a private function used to calculate offset and slot recursively. 
    '''
    def __find_item(self,path,current_type,current_slot,current_offset):
        origin_type=self.origin_types[current_type]
        if 'mapping' == origin_type['encoding']:
            key_type=self.origin_types[origin_type['key']]
            key_size=key_type['numberOfBytes']
            key=path[0].to_bytes(int(32),byteorder='big')
            offset=current_slot.to_bytes(32,byteorder='big')
            all_offset=key+offset
            k = keccak_256()
            k.update(all_offset)
            whole_offset=k.hexdigest()
            value_type=origin_type['value']
            a,b,value_size,types=self.__find_item(path[1:],value_type,int(whole_offset,16),0)
            return a,b,value_size,types
        if 'dynamic_array' == origin_type['encoding']:
            key=path[0].to_bytes(32,byteorder='big')
            offset=current_slot.to_bytes(32,byteorder='big')
            all_offset=key+offset
            k = keccak_256()
            k.update(all_offset)
            whole_offset=k.hexdigest()
            value_type=origin_type['base']
            a,b,value_size,types=self.__find_item(path[1:],value_type,int(whole_offset,16),0)
            return a,b,value_size,types
        if 't_array' in current_type:
            offset=current_offset
            slot=current_slot
            idx=int(path[0])
            base=origin_type['base']
            per_size=int(self.origin_types[base]['numberOfBytes'])
            for i in range(idx):
                if offset+per_size>32:
                    slot=slot+1
                    offset=0
                offset+=per_size;
            return slot,offset,per_size,self.origin_types[base]['label']
        if 't_struct' in current_type :
            current_member=path[0]
            member={}
            for i in origin_type['members']:
                if i['label']==current_member:
                    member=i
                    break
            offset_=int(member['offset'])+current_offset
            slot_=int(member['slot'])+current_slot
            value_type=member['type']
            a,b,value_size,types=self.__find_item(path[1:],value_type,slot_,offset_)
            return a,b,value_size,types
        else:
            return current_slot,current_offset,self.origin_types[current_type]['numberOfBytes'],self.origin_types[current_type]['label']
            
    '''
        query calculates offset and slot for arbitrary storage variables. 
        parameters: contract_name: which contract dose the variable belongs to. (One sourcefile may contain many contracts).
        return values: slot, offset,err. If 'err' is True, then some error occurs during the execution, offset and slot will be set to -1.
    '''
    def query(self,contract_name_, path):
        contract_name='file:'+contract_name_
        origin_label=path[0]
        origin_type_dict={}
        for i in self.origin_location:
            if i['label'] == origin_label and i['contract'] == contract_name:
                origin_type_dict=i;
                break;  
        if origin_type_dict == {}:
            # logging.warning("No such variable: %s"%path[0])
            # return -1,-1,-1,'',False
            raise Exception("No such variable: %s"%path[0])
        try:
            slot,offset,value_size,types=self.__find_item(path[1:],origin_type_dict['type'],int(origin_type_dict['slot']),int(origin_type_dict['offset']))
        except:
            # logging.warning("Cannot calculate offset and slot: unsupported variable: %s or invalid access path"%path[0])
            # return -1,-1,-1,'',False
            raise Exception("Cannot calculate offset and slot: unsupported variable: %s or invalid access path"%path[0])
        return slot,offset,value_size,types,True

    '''
    get_all_static_variable calculates all variables for fixed-size variables and the placeholders of mappings or dynamic arrays
    return values: a list, each element is a dict like :{'name':variable_name,'offset':offset,'slot':slot}
    '''
    def get_all_static_variables(self,contract_name_):
        contract_name='file:'+contract_name_
        res=[]
        try:
            for v in self.origin_location:
                if v['contract'] == contract_name:
                    res.append({'name':v['label'],'offset':v['offset'],'slot':v['slot'],'size':self.origin_types[v['type']]['numberOfBytes'],'type':self.origin_types[v['type']]['label']})
        except: 
            # logging.warnings("The output of solc is incomplete, please check your solc version")
            raise Exception("The output of solc is incomplete, please check your solc version")
        return res

