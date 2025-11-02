from .models import Cross, CrossNamingRule, ProgenyNamingRule


def get_progeny_phenotype_name(cross: Cross, genotype: str) -> str:
    """
    Determines the phenotype name for a progeny by querying the database.
    """
    variety1 = cross.parent1.variety
    variety2 = cross.parent2.variety

    # Always query for the rule with the varieties sorted consistently.
    # This handles the case where parent1 and parent2 are swapped in a different Cross object.
    sorted_varieties = sorted([variety1, variety2], key=lambda v: v.id)

    # Check if a custom naming rule exists for this cross.
    try:
        cross_rule = CrossNamingRule.objects.get(
            variety1=sorted_varieties[0], variety2=sorted_varieties[1]
        )

        # If a rule is found, try to get the phenotype name for the specific genotype.
        progeny_rule = ProgenyNamingRule.objects.get(
            cross_rule=cross_rule, genotype_pattern=genotype
        )
        return progeny_rule.phenotype_name

    except (CrossNamingRule.DoesNotExist, ProgenyNamingRule.DoesNotExist):
        pass  # No specific rule found, fall through to default logic.

    # Fallback to a generic name for unnamed crosses
    return f"{variety1.species} ({variety1.name} X {variety2.name})"
