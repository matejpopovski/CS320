# project: p3
# submitter: popovski
# partner: none
# hours: 10

from collections import deque
import os
import pandas as pd
import time
import requests
from selenium.webdriver.common.by import By

class GraphSearcher:
    def __init__(self):
        self.visited = set()
        self.order = []

    def visit_and_get_children(self, node):
        raise Exception("must be overridden in sub classes -- don't change me here!")

    def dfs_search(self, node):
        self.visited.clear()
        self.order.clear()
        self.dfs_visit(node)
        return self.order
    
    def dfs_visit(self, node):
        if node in self.visited:
            return
        self.visited.add(node)
        children = self.visit_and_get_children(node)
        for child in children:
            self.dfs_visit(child)
    
    def bfs_search(self, node):
        self.visited.clear()
        self.order.clear()
        self.bfs_visit(node)
        return self.order

    def bfs_visit(self, node):
        q = deque([node])
        while q:
            node = q.popleft()
            if node in self.visited:
                continue
            children = self.visit_and_get_children(node)
            q.extend(children)

class MatrixSearcher(GraphSearcher):
    def __init__(self, df):
        super().__init__()
        self.df = df
        
    def visit_and_get_children(self, node):
        children = []
        for child, has_edge in self.df.loc[node].items():
            if has_edge and child not in self.visited:
                children.append(child)
        self.visited.add(node)
        self.order.append(node)
        return children

class FileSearcher(GraphSearcher):
    def __init__(self):
        super().__init__()
        
    def visit_and_get_children(self, file):
        with open(os.path.join('file_nodes', file)) as f:
            value = f.readline().strip()
            children_str = f.readline().strip()
            
        self.visited.add(file)
        self.order.append(value)
        children = [file for file in children_str.split(',') if file not in self.visited]
        
        return children
    
    def concat_order(self):
        ret =""
        for value in self.order:
            ret += value
        return ret

    
class WebSearcher(GraphSearcher):
    def __init__(self, driver):
        super().__init__()
        self.driver = driver
        self.table_fragments = []
        self.visited_nodes = set()

    def visit_and_get_children(self, node):
        if node in self.visited_nodes:
            return []  

        self.driver.get(node)
        self.visited_nodes.add(node)

        urls = []
        for link in self.driver.find_elements(by = 'tag name', value = 'a'):
            url = link.get_attribute('href')
            if url:
                urls.append(url)

        fragment = self.driver.page_source
        self.table_fragments.append(fragment)
        self.order.append(node)

        return urls

    def table(self):
        dfs = []
        for fragment in self.table_fragments:
            df = pd.read_html(fragment)[0]
            dfs.append(df)

        return pd.concat(dfs, ignore_index=True)


    
def reveal_secrets(driver, url, travellog):
    password = ""
    for digit in travellog["clue"]:
        digit_str = str(digit)
        password += str(digit_str)  
    driver.get(url)
    password_textbox = driver.find_element(By.ID, 'password-textbox')
    password_textbox.send_keys(password)
    submit_button = driver.find_element(By.ID, 'submit-button')
    submit_button.click()
    time.sleep(3)
    location_button = driver.find_element(By.ID, 'view-location-button')
    location_button.click()
    time.sleep(3)
    
    image_url = driver.find_element(by=By.TAG_NAME, value='img').get_attribute('src')
    request = requests.get(image_url)

    with open("Current_Location.jpg", "wb") as file:
        file.write(request.content)
    current_location = driver.find_element(By.ID, 'location').text
    return current_location