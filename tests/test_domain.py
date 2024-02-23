import iroha
import time

def start_client():
    key_pair = iroha.KeyPair.from_json("""
    {
      "public_key": "ed01207233BFC89DCBD68C19FDE6CE6158225298EC1131B6A130D1AEB454C1AB5183C0",
      "private_key": {
        "digest_function": "ed25519",
        "payload": "9ac47abf59b356e0bd7dcbbbb4dec080e302156a48ca907e47cb6aea1d32719e7233bfc89dcbd68c19fde6ce6158225298ec1131b6a130d1aeb454c1ab5183c0"
      }
    }
    """)
    
    account_id = "alice@wonderland"
    web_login = "mad_hatter"
    password = "ilovetea"
    api_url = "http://127.0.0.1:8080/"
    telemetry_url = "http://127.0.0.1:8180/"
    
    client = iroha.Client.create(
                key_pair,
                account_id,
                web_login,
                password,
                api_url)
    return client

def test_register_account():
    client = start_client()

    domains = client.query_all_domains()
    
    print("Listing all domains...")
    for d in domains:
        print(" - ", d,)
    
    domain_id = "looking_glass_" + str(len(domains))
    
    if domain_id in domains:
        print("'" + domain_id +"' domain already exists.")

    register = iroha.Instruction.register_domain(domain_id)
    
    client.submit_executable([register])

    for x in range(30):
        domains = client.query_all_domains()
        
        if domain_id in domains:
            break
        
        time.sleep(1)
        
    assert domain_id in domains
    