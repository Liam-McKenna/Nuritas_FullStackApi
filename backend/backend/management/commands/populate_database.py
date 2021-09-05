"""
Populate models for demo.
"""
import random
import string

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group

from peptides import models


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Create users
        print(f"Creating users...")
        password = 'testtest'
        a = User.objects.create(
            first_name='Andy',
            last_name='Scientist',
            username='andy_scientist',
            password=password
        )
        j = User.objects.create(
            first_name='John',
            last_name='Engineer',
            username='john_engineer',
            password=password
        )
        m = User.objects.create(
            first_name='Mary',
            last_name='Manager',
            username='mary_manager',
            password=password
        )

        scientists = Group.objects.create(name='Scientists')
        users = Group.objects.create(name='Users')

        scientists.user_set.set([a])
        users.user_set.set([a, j, m])

        print('Created Users:')
        print('\t-andy_scientist in groups ', ', '.join([g.name for g in a.groups.all()]))
        print('\t-john_engineer in groups ', ', '.join([g.name for g in j.groups.all()]))
        print('\t-mary_manager in groups ', ', '.join([g.name for g in m.groups.all()]))
        print('\tall passwords set to "testtest"')

        number = 0
        peptides = {}
        for i in range(1, 101):
            number += 1
            if number % 8 == 0 or number % 11 == 0:
                number += 1
            sequence = ''.join(
                random.choice(string.ascii_uppercase)
                for _ in range(random.randint(5, 20))
            )
            peptides[i] = models.Peptide.objects.create(
                name=f'pep_{number}',
                sequence=sequence
            )

        print('Generated 100 peptides')

        assays = []
        for i in range(1, 6):
            peps = [peptides[p] for p in range(1, 101) if p % i == 0]
            assay = models.Assay.objects.create(
                name=f"Assay {i}",
                operator=a
            )
            assay.peptides.set(peps)
            assays.append(assay)

        print(f'Generated {len(assays)} assays')
        for assay in assays:
            print(f'\t Assay "{assay.name}" done by {assay.operator.get_full_name()} with {len(assay.peptides.all())} peptides')

        print("Done!")
