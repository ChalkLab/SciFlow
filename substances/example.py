"""example functions for development"""
import os
import django
import time
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sciflow.settings")
django.setup()
from substances.views import *
from datafiles.df_functions import *
from substances.external import *
from scyjava import config, jimport
from workflow.gdb_functions import *


# add a new substance jld to the database
runjld = True
if runjld:
    subs = Substances.objects.all().order_by('id')
    for sub in subs:
        if sub.graphdb is None:
            continue
        facet = FacetLookup.objects.get(id=sub.facet_lookup_id)
        if facet.currentversion == 1:
            subid = sub.id
            # generate new json-ld file (as python dictionary)
            jld = createsubjld(subid)
            jld["@id"] = sub.graphdb  # updating the graphname from the initial ingest
            # get the latest version of this file from facet_files
            lastver = FacetFiles.objects.filter(facet_lookup_id=sub.facet_lookup_id).order_by('-version')[0]
            newver = lastver.version + 1
            # load into facet_files
            file = FacetFiles(facet_lookup_id=sub.facet_lookup_id,
                              file=json.dumps(jld, separators=(',', ':')), type='raw', version=newver)
            file.save()
            # add json-ld to the graph replacing the old version
            addgraph('facet', sub.facet_lookup_id, 'remote', sub.graphdb)
            # update facet_lookup
            lookup = FacetLookup.objects.get(id=sub.facet_lookup_id)
            lookup.currentversion = newver
            lookup.save()
            print("Updated '" + sub.graphdb + "'")
            time.sleep(3)
        else:
            print("Already updated '" + sub.graphdb + "'")

# add a new substance to the database
add = None
if add:
    # example substance that is not found online...
    meta = {
        "name": "sodium gadolinium titanate",
        "formula": "GdNaO4Ti",
        "molweight": 292.104,
        "iupacname": "Gadolinium sodium titanium oxide",
        "inchi": "InChI=1S/Gd.Na.4O.Ti/q+3;+1;4*-2;+4",
        "inchikey": "HZKODDDQUJIOQB-UHFFFAOYSA-N"
    }
    key = "HZKODDDQUJIOQB-UHFFFAOYSA-N"
    added = addsubstance(key)

    if not added:
        print("Substance not added")
        print(added)
        exit()

    # generate the JSON-LD file for the substance
    subid = added.id
    jsonld = createsubjld(subid)

    # store the JSON-LD in the facet_lookups/facet_files tables
    facetid = addfacetfile(jsonld)

    # update facet file with the facet_id
    jsonld['@id'] = jsonld['@id'].replace('<facetid>', str(facetid))

    # save the facet file to the facet_file table
    saved = updatefacetfile(jsonld)
    if saved:
        print("Facet JSON-LD saved to the DB!")
    else:
        print("Error: something happened on the way to the DB!")

# check output of pubchem request
runpc = None
if runpc:
    key = 'VWNMWKSURFWKAL-HXOBKFHXSA-N'
    meta, ids, descs, srcs = {}, {}, {}, {}
    pubchem(key, meta, ids, descs, srcs)
    print(meta, ids, descs)
    print(json.dumps(srcs, indent=4))

# check output of chembl request
runcb = None
if runcb:
    key = 'REEUVFCVXKWOFE-UHFFFAOYSA-K'
    # key = 'aspirin'
    meta, ids, descs, srcs = {}, {}, {}, {}
    chembl(key, meta, ids, descs, srcs)
    print(meta, ids, descs)
    print(json.dumps(srcs, indent=4))

# check output of classyfire request
runcf = None
if runcf:
    key = 'VWNMWKSURFWKAL-HXOBKFZXSA-N'  # (bad inchikey)
    descs, srcs = {}, {}
    classyfire(key, descs, srcs)
    print(descs)
    print(json.dumps(srcs, indent=4))

# check output of wikidata request
runwd = None
if runwd:
    key = 'BSYNRYMUTXBXSQ-CHALKCHALK-N'  # (bad inchikey for aspirin)
    ids, srcs = {}, {}
    wikidata(key, ids, srcs)
    print(ids)
    print(json.dumps(srcs, indent=4))

# Get data from commonchemistry using CASRNs
runcc1 = None
if runcc1:
    subs = Substances.objects.all().values_list(
        'id', 'casrn').filter(
        casrn__isnull=False)  # produces tuples
    for sub in subs:
        found = Sources.objects.filter(
            substance_id__exact=sub[0],
            source__exact='comchem')
        if not found:
            meta, ids, srcs = {}, {}, {}
            comchem(sub[1], meta, ids, srcs)
            saveids(sub[0], ids)
            savesrcs(sub[0], srcs)
            print(sub)
            print(json.dumps(srcs, indent=4))

runcc2 = None
if runcc2:
    # process compounds with no casrn in substances table
    subs = Substances.objects.all().values_list(
        'id', flat=True).filter(
        casrn__isnull=True)
    for sub in subs:
        found = Sources.objects.filter(
            substance_id__exact=sub,
            source__exact='comchem')
        if not found:
            key = getinchikey(sub)
            if key:
                meta, ids, srcs = {}, {}, {}
                if comchem(key, meta, ids, srcs):
                    saveids(sub, ids)
                    # update casrn field in substances
                    updatesubstance(sub, 'casrn', ids['comchem']['casrn'])
                    print('CASRN updated')
                savesrcs(sub, srcs)
                print(sub)
                print(json.dumps(srcs, indent=4))
            else:
                print(sub)

runlm = None
if runlm:
    apipath = "https://commonchemistry.cas.org/api/detail?cas_rn="
    f = open("reach_ids.txt", "r")
    for line in f:
        parts = line.replace('\n', '').split(':')
        print(parts)
        res = requests.get(apipath + parts[1])
        if res.status_code == 200:
            with open(parts[0] + '.json', 'w') as outfile:
                json.dump(res.json(), outfile)
                print('Found')
        else:
            print('Not found')

# check output of getinchikey function
rungi = None
if rungi:
    subid = 1
    out = getinchikey(subid)
    print(out)

# test scyjava
runsj = None
if runsj:
    config.add_endpoints('io.github.egonw.bacting:managers-cdk:0.0.16')
    workspaceRoot = "."
    cdkClass = jimport("net.bioclipse.managers.CDKManager")
    cdk = cdkClass(workspaceRoot)

    print(cdk.fromSMILES("CCC"))

runls = None
if runls:
    subview(None, 5044)
