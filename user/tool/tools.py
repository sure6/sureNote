# coding=utf-8
"""
date: 2021/8/10 14:45
author: lee sure
"""
import hashlib



def md5_encryption_tool(st):
    # 哈希算法, 给定明文, 计算出一段定长, 不可逆的值, md5, sha-256
    # 特点:1, 定长输出，不管密码多长，输出长度都一样， md5采用32位16进制
    # 2， 不可逆: 无法反向计算出, 对应的明文
    # 3， 雪崩效应: 输入改变, 输出必然变
    # 场景: 1, 密码处理 2, 文件完整性校验

    # md5 加密
    if st is None:
        return
    # 创建一个加密对象
    m = hashlib.md5()
    # 对字符串进行采用2进制更新操作, 如果在同一加密对象下
    # 采用update操作,实质是在源字符串上累加,加密
    m.update(st.encode())
    # 返回加密的32位16进制的值
    return m.hexdigest()

if __name__=="__main__":
    print(md5_encryption_tool("123"))
    print(md5_encryption_tool("123"))