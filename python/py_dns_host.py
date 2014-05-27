
#/*******************************************************************************
# * Author	 : jingbo.li | work at r
# * Email	 : ljb90@live.cn
# * Last modified : 2014-05-27 17:37
# * Filename	 : py_dns_host.py
# * Description	 : 对于url指定host的DNS解析
# * *****************************************************************************/

import DNS

def fetch_dns(url, dns_server):
    url = urlparse(url)
    out = DNS.Request(name=str(url[1]), server=str(dns_server))
    resolve = out.req(timeout=1).answers
    for ips in resolve:
        print ips['data']

fetch_dns('','')
