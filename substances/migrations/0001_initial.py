# Generated by Django 3.2.5 on 2021-07-10 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Descriptors',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(default='', max_length=128)),
                ('value', models.CharField(default='', max_length=768)),
                ('source', models.CharField(default='', max_length=64)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'descriptors',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Identifiers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('casrn', 'CAS Registry Number'), ('inchi', 'IUPAC InChI String'), ('inchikey', 'IUPAC InChI Key'), ('csmiles', 'Canonical SMILES'), ('ismiles', 'Isomeric SMILES'), ('chemspider', 'Chemspider ID'), ('pubchem', 'PubChem Compound ID'), ('iupacname', 'IUPAC Name'), ('springer', 'Springer ID'), ('othername', 'Other Name'), ('atc', 'ATC Code'), ('reaxys', 'Reaxys ID'), ('gmelin', 'Gmelin ID'), ('chebi', 'ChEBI ID'), ('chembl', 'ChEMBL ID'), ('rtecs', 'RTECS ID'), ('dsstox', 'DSSTOX ID')], default='casrn', max_length=10)),
                ('value', models.CharField(default='', max_length=768)),
                ('iso', models.CharField(default=None, max_length=5)),
                ('source', models.CharField(default='', max_length=64)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'identifiers',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Sources',
            fields=[
                ('id', models.AutoField(db_column='Id', primary_key=True, serialize=False)),
                ('source', models.CharField(max_length=32)),
                ('result', models.CharField(max_length=1)),
                ('notes', models.CharField(blank=True, max_length=2000, null=True)),
                ('updated', models.DateTimeField()),
            ],
            options={
                'db_table': 'sources',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Structures',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('molfile', models.TextField()),
                ('updated', models.DateTimeField()),
            ],
            options={
                'db_table': 'structures',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Substances',
            fields=[
                ('id', models.SmallAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=256)),
                ('formula', models.CharField(default='', max_length=256)),
                ('monomass', models.FloatField(default=0.0)),
                ('molweight', models.FloatField(default=0.0)),
                ('casrn', models.CharField(default='', max_length=16)),
                ('graphdb', models.CharField(max_length=256, null=True)),
                ('facet_lookup_id', models.IntegerField(blank=True, null=True)),
                ('comments', models.CharField(max_length=256, null=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'substances',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SubstancesSystems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(blank=True, max_length=13, null=True)),
                ('constituent', models.PositiveIntegerField(blank=True, null=True)),
                ('mixture_id', models.IntegerField(blank=True, null=True)),
                ('updated', models.DateTimeField()),
            ],
            options={
                'db_table': 'substances_systems',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Systems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=1024)),
                ('composition', models.CharField(choices=[('PS', 'pure compound'), ('BM', 'binary mixture'), ('TM', 'ternary mixture'), ('QM', 'quaternary mixture'), ('NM', 'quinternary mixture')], default='PS', max_length=2)),
                ('identifier', models.CharField(default='', max_length=128)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'systems',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Templates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=16)),
                ('json', models.TextField()),
                ('version', models.SmallIntegerField()),
                ('updated', models.DateTimeField()),
            ],
            options={
                'db_table': 'templates',
                'managed': False,
            },
        ),
    ]
