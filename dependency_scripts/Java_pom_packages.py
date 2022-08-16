import os




def pomParse(results):
    # loop through pom files and find dependencies or dependency management sections and parse them
    depMan = []
    dep = []
    finalement = {
                    "artifact_id": [],
                    "group_id": [],
                    "version": [],
                    "scope": [],
                    }

    final  = {
        "artifact_id": [],
        "group_id": [],
        "version": [],
        "scope": [],
    }
    for a in results:
        # get all the key value pairs in a 
        for key, value in a.items():
            for k,v in value.items():
                if k == "dependencyManagement":
                    depMan.append(v)
                if k == "dependencies":
                    dep.append(v)
    for fgh in dep:
        try:
            for key, value in fgh.items():
                # get all the key value pairs in a from list of dictionaries
                if key:
                        for i in value:
                            # get all the key value pairs in a from list of dictionaries
                            for k,v in i.items():
                                if k == "artifactId":
                                    finalement["artifact_id"].append(v)
                                if k == "groupId":
                                    finalement["group_id"].append(v)
                                if k == "version":
                                    finalement["version"].append(v)
                                if k == "scope":
                                    finalement["scope"].append(v)
        except:
            pass
    for bbr in depMan:
        # get all the key value pairs in a from list of dictionaries
        for key, value in bbr.items():
            if key:
                for i, a in value.items():
                    for g in a:
                        for k,v in g.items():
                            if k == "artifactId":
                                final["artifact_id"].append(v)
                            if k == "groupId":
                                final["group_id"].append(v)
                            if k == "version":
                                final["version"].append(v)
                            if k == "scope":
                                final["scope"].append(v)

    return finalement, final
