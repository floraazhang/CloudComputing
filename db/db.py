import azure.cosmos.cosmos_client as cosmos_client

def getdata():
    config = {
        'ENDPOINT': 'https://estruscosmosdb.documents.azure.com:443/',
        'PRIMARYKEY': 'R2M6nKvkUKf4vYohKEr2hph74zDMVD9i4mQT2wTyKSE8kYdZ3NAHNlth1Fz0BZ1vaYnCgamLRnYhOZ5B33A8nQ==',
        'DATABASE': 'estruscosmosdb',
        'CONTAINER': 'EstrusStatus'
    }

    # Initialize the Cosmos client
    client = cosmos_client.CosmosClient(url_connection=config['ENDPOINT'], auth={
                                        'masterKey': config['PRIMARYKEY']})

    # Create a database
    db = list(client.QueryDatabases("select * from c where c.id='estruscosmosdb'"))

    # Create container options
    options = {
        'offerThroughput': 400
    }

    container_definition = {
        'id': config['CONTAINER']
    }

    # Create a container
    #container = client.CreateContainer(db['_self'], container_definition, options)
    container=list(client.QueryContainers(db[0]['_self'],"select * from c where c.id='EstrusStatus'",options))

    # Query these items in SQL
    query = {'query': "SELECT * FROM c"}

    options = {}
    options['enableCrossPartitionQuery'] = True
    options['maxItemCount'] = 2

    result_iterable = client.QueryItems(container[0]['_self'], query, options)
    data=[]
    for item in iter(result_iterable):
        row={}
        row['cowId']=item['cowId']
        row['probability']=item['probability']
        row['label']=item['estrusLabel']
        row['hour_temp']=item['hour_stomach_temp_celcius']
        row['activity']=item['hour_animal_activity']
        row['hour_low_pass_over_activity']=item['hour_low_pass_over_activity']
        row['hour_temp_without_drink_cycles']=item['hour_temp_without_drink_cycles']
        data.append(row)


    data.sort(key=lambda a:-a['probability'])
    return data

def search_cow_byID(ID):
    config = {
        'ENDPOINT': 'https://estruscosmosdb.documents.azure.com:443/',
        'PRIMARYKEY': 'R2M6nKvkUKf4vYohKEr2hph74zDMVD9i4mQT2wTyKSE8kYdZ3NAHNlth1Fz0BZ1vaYnCgamLRnYhOZ5B33A8nQ==',
        'DATABASE': 'estruscosmosdb',
        'CONTAINER': 'RawDataCollection'
    }

    # Initialize the Cosmos client
    client = cosmos_client.CosmosClient(url_connection=config['ENDPOINT'], auth={
                                        'masterKey': config['PRIMARYKEY']})

    # Create a database
    db = list(client.QueryDatabases("select * from c where c.id='estruscosmosdb'"))

    # Create container options
    options = {
        'offerThroughput': 400
    }

    container_definition = {
        'id': config['CONTAINER']
    }

    # Create a container
    #container = client.CreateContainer(db['_self'], container_definition, options)
    container=list(client.QueryContainers(db[0]['_self'],"select * from c where c.id='RawDataCollection'",options))

    query = {'query': "SELECT * FROM c where c.cowId='%d'" % ID} 

    options = {}
    options['enableCrossPartitionQuery'] = True
    options['maxItemCount'] = 2

    result_iterable = client.QueryItems(container[0]['_self'], query, options)
    data=[]
    for item in iter(result_iterable):
        row={}
        row['cowId']=item['cowId']
        row['hour_temp']=item['hour_stomach_temp_celcius']
        row['activity']=item['hour_animal_activity']
        row['hour_low_pass_over_activity']=item['hour_low_pass_over_activity']
        row['hour_temp_without_drink_cycles']=item['hour_temp_without_drink_cycles']
        row['label']=item['label']
        row['timestamp']=item['timestamp']
        row['recordID']=item['_rid']
        row['documentID']=item['id']
        data.append(row)


    return data

def GetDatabaseLink(self, database, is_name_based=True):
    if is_name_based:
        return 'dbs/' + database['id']
    else:
        return database['_self']

def GetDocumentCollectionLink(self, database, document_collection, is_name_based=True):
        if is_name_based:
            return self.GetDatabaseLink(database) + '/colls/' + document_collection['id']
        else:
            return document_collection['_self']

def GetDocumentLink(database, document_collection, id, is_name_based=True):
    if is_name_based:
        return 'dbs/' + database + '/colls/' + document_collection + '/docs/' + str(id)
    else:
        return id

def updateMLModel(parameters):
    config = {
        'ENDPOINT': 'https://estruscosmosdb.documents.azure.com:443/',
        'PRIMARYKEY': 'R2M6nKvkUKf4vYohKEr2hph74zDMVD9i4mQT2wTyKSE8kYdZ3NAHNlth1Fz0BZ1vaYnCgamLRnYhOZ5B33A8nQ==',
        'DATABASE': 'estruscosmosdb',
        'CONTAINER': 'MachineLearningModel'
    }

    # Initialize the Cosmos client
    client = cosmos_client.CosmosClient(url_connection=config['ENDPOINT'], auth={
                                        'masterKey': config['PRIMARYKEY']})

    # Create a database
    db = list(client.QueryDatabases("select * from c where c.id='estruscosmosdb'"))

    # Create container options
    options = {
        'offerThroughput': 400
    }

    container_definition = {
        'id': config['CONTAINER']
    }

    # Create a container
    #container = client.CreateContainer(db['_self'], container_definition, options)
    container=list(client.QueryContainers(db[0]['_self'],"select * from c where c.id='MachineLearningModel'",options))
    print(container[0]['_self'])
    options = {}
    options['enableCrossPartitionQuery'] = True
    options['maxItemCount'] = 2
    
    documentLink = "dbs/5tsxAA==/colls/5tsxAI8VKaU=/docs/5tsxAI8VKaUBAAAAAAAAAA=="
    replace_document = {}
    replace_document['id'] = '1'
    replace_document['stemp_C'] = parameters['stemp_C']
    replace_document['animal_activity_C'] = parameters['animal_activity_C']
    replace_document['low_pass_over_activity_C'] = parameters['low_pass_over_activity_C']
    replace_document['temp_without_drink_cycles_C'] = parameters['temp_without_drink_cycles_C']

    replaced_document = client.ReplaceItem(documentLink, replace_document)
    print("Machine Learning Model Updated")
    return "Machine Learning Model Updated"

def updateLabelByRids(identifiers):
    config = {
        'ENDPOINT': 'https://estruscosmosdb.documents.azure.com:443/',
        'PRIMARYKEY': 'R2M6nKvkUKf4vYohKEr2hph74zDMVD9i4mQT2wTyKSE8kYdZ3NAHNlth1Fz0BZ1vaYnCgamLRnYhOZ5B33A8nQ==',
        'DATABASE': 'estruscosmosdb',
        'CONTAINER': 'RawDataCollection'
    }

    # Initialize the Cosmos client
    client = cosmos_client.CosmosClient(url_connection=config['ENDPOINT'], auth={
                                        'masterKey': config['PRIMARYKEY']})

    # # Create a database
    # db = list(client.QueryDatabases("select * from c where c.id='estruscosmosdb'"))

    # # Create container options
    # options = {
    #     'offerThroughput': 400
    # }

    # container_definition = {
    #     'id': config['CONTAINER']
    # }

    # Create a container
    #container = client.CreateContainer(db['_self'], container_definition, options)
    # container=list(client.QueryContainers(db[0]['_self'],"select * from c where c.id='RawDataCollection'",options))

    collectionLink = "dbs/5tsxAA==/colls/5tsxAINrOBA=/docs/"
    for identifier in identifiers:
        print(identifier)
        options = { 'partitionKey': identifier['id'] }
        documentLink = 'dbs/5tsxAA==/colls/5tsxAI8VKaU=/docs/' + identifier['rid']
        print(documentLink)
        targetItem = client.ReadItem(documentLink, options)
        targetItem['label'] = 0 if targetItem['label'] == 1 else 1
        updated_Item = client.ReplaceItem(documentLink, targetItem)
    
    print("Data Labels Updated")
    return "Selected Data Relabeled"
    
