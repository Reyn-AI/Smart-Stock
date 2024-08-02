

stock_list_store = {}  #存储股票列表信息用于分页 key是uuid
order_list_store = {} #交割单表分页缓存

def get_items():
    if len(stock_list_store)>10:
        del stock_list_store[list(stock_list_store.keys())[0]]
    return stock_list_store

def get_order_cache():
    if len(order_list_store)>10:
        del order_list_store[list(order_list_store.keys())[0]]
    return order_list_store

def store_order_data(uuid, infos:list):
    """存储订单数据"""
    order_list_store[uuid] = infos

def store_data(uuid, infos:dict):
    """存储数据"""
    stock_list_store[uuid] = infos

def get_order_by_index(uuid, start, length, items: dict):
    """交割单信息索引"""
    res = []
    try:
        data = items.get(uuid)
        if start>= len(data):
            pass
        elif (start+length)>= len(data):
            res = data[start:]
        else:
            res = data[start:start+length]

    except Exception as e:
        print(e)
    finally:
        return res

def get_by_index(uuid, tab_name, start, length, items: dict):
    """通过索引取数据"""
    res = []
    try:
        data = items.get(uuid)
        tab_data = data.get(tab_name, [])
        if start>= len(tab_data):
            pass
        elif (start+length)>= len(tab_data):
            res = tab_data[start:]
        else:
            res = tab_data[start:start+length]

    except Exception as e:
        print(e)
    finally:
        return res

def delete_cache(uuid, items:dict):
    """删除缓存"""
    if uuid in items.keys():
        del items[uuid]
        return True
    return False
