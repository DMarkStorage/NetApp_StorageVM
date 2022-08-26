# NetApp_StorageVM
Python program that connects to NetApp server using RestAPI, lets user create, remove and get the details of a Storage VM from NetApp server.


### Features
- `CREATE` a StorageVM into a given storage
- `DELETE` a StorageVM into a given storage
- Get the `LIST` of StorageVMs
- Helpful CLI

### Requirements
- Python 3.6 or higher
- ONTAP 9 (NetApp storage system) or higher (untested on earlier versions)
- Install docopt

Check [install docopt](https://pypi.org/project/docopt/) for more information


### Usage Example
## Run the program


1. Creating a StorageVM

```bash
netapp_SVM.py -s [STORAGE] -VM [SVM]  --create
```

2. Remove a StorageVM
```bash
netapp_SVM.py -s [STORAGE] -VM [SVM]  --remove
```

3. GET a list of all StorageVM
```bash
netapp_SVM.py -s [STORAGE] -VM [SVM] --list
```
    		

4. HELP
```
netapp_SVM.py -h | --help
```

- [STORAGE] => name of your storage
- [SVM] => name of StorageVM

##FLOWCHART

```mermaid
flowchart LR
    S([START]) --> IO[/INPUT<br>Storage<br>Filesystem<br>Snapshot<br>Operation:<br><i>CREATE,REMOVE,GETDETAILS/]
    IO --> CR[CREATE]
    CR --> CHK{If StorageVM exist}
    CHK --YES--> X{SVM Exist}
    X --YES--> CRX>SVM Exist]
    CHK --NO--> VL{If StorageVM name valid}
    VL --YES--> OUT>CRETED]
    VL --NO--> IV>Invalid StorageVM name]
    IO --> RM[REMOVE]
    RM --> CHK
    CHK --YES--> X
    X --YES--> ID[GET UUID]
    ID --> DEL[DELETE StorageVM]
    CHK --NO--> NX>Does not Exist]
    IO --> DT[DETAILS]
    DT --> CHK
    CHK --YES--> X
    X --> dtls>Show Details]
    CHK --NO--> NX



style CR stroke:green,stroke-width:1px
style RM stroke:red,stroke-width:1px
style DT stroke:blue,stroke-width:1px

linkStyle 1 stroke-width:2px,fill:none,stroke:green;
linkStyle 2 stroke-width:2px,fill:none,stroke:green;
linkStyle 3 stroke-width:2px,fill:none,stroke:green;
linkStyle 4 stroke-width:2px,fill:none,stroke:green;
linkStyle 5 stroke-width:2px,fill:none,stroke:green;
linkStyle 6 stroke-width:2px,fill:none,stroke:green;
linkStyle 7 stroke-width:2px,fill:none,stroke:green;

linkStyle 8 stroke-width:2px,fill:none,stroke:red;
linkStyle 9 stroke-width:2px,fill:none,stroke:red;
linkStyle 10 stroke-width:2px,fill:none,stroke:red;
linkStyle 11 stroke-width:2px,fill:none,stroke:red;
linkStyle 12 stroke-width:2px,fill:none,stroke:red;
linkStyle 13 stroke-width:2px,fill:none,stroke:red;

linkStyle 14 stroke-width:2px,fill:none,stroke:blue;
linkStyle 15 stroke-width:2px,fill:none,stroke:blue;
linkStyle 16 stroke-width:2px,fill:none,stroke:blue;
linkStyle 17 stroke-width:2px,fill:none,stroke:blue;
linkStyle 18 stroke-width:2px,fill:none,stroke:blue;











```