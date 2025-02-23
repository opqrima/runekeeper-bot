import re

def parse_airdrop_message(message_text: str) -> dict:
    lines = message_text.split('\n')
    
    header_match = re.match(r'AIRDROP ASC, \[(.*?)\](.*)', lines[0])
    if not header_match:
        return None
        
    date_str = header_match.group(1)
    
    project_info = lines[1].strip()
    project_name = ""
    category = ""
    
    # Clean up project name
    project_info = re.sub(r'^\[.*?\]\s*', '', project_info)  # Remove category tags
    project_info = re.sub(r'^(?:New\s+)?(?:Airdrop[s]?|Testnet|Early\s+Acces[s]?):\s*', '', project_info)  # Remove prefixes
    # Remove emojis and other special characters
    project_info = re.sub(r'[\U0001F300-\U0001F9FF\U0001F600-\U0001F64F\U0001F680-\U0001F6FF\u2600-\u26FF\u2700-\u27BF👋]', '', project_info)
    project_name = project_info.strip()
    
    reward = ""
    tasks = []
    
    category_matches = re.match(r'\[(.*?)\](.*)', project_info)
    if category_matches:
        category = category_matches.group(1).strip()
        project_name = category_matches.group(2).strip()
    else:
        project_name = project_info
    
    links = []
    for line in lines:
        if 'http' in line:
            url_match = re.search(r'(https?://\S+)', line)
            if url_match:
                links.append(url_match.group(1))
        
        if 'Reward' in line:
            reward = line
        
        if line.strip().startswith('➡️') or line.strip().startswith('🟢') or line.strip().startswith('➖'):
            tasks.append(line.strip())
    
    return {
        'project_name': project_name,
        'category': category,
        'date_posted': date_str,
        'link': links[0] if links else '',
        'description': '\n'.join(lines[1:]),
        'reward': reward,
        'tasks': '\n'.join(tasks)
    }