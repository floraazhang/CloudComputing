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


    # Create and add some items to the container
    # item1 = client.CreateItem(container['_self'], {
    #     'id': 'server1',
    #     'Web Site': 0,
    #     'Cloud Service': 0,
    #     'Virtual Machine': 0,
    #     'message': 'Hello World from Server 1!'
    #     }
    # )

    # item2 = client.CreateItem(container['_self'], {
    #     'id': 'server2',
    #     'Web Site': 1,
    #     'Cloud Service': 0,
    #     'Virtual Machine': 0,
    #     'message': 'Hello World from Server 2!'
    #     }
    # )

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

    query = {'query': "SELECT * FROM c where c.cowId='%d'"%ID} 

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


    return data[0]
