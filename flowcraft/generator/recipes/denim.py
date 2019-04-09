try:
    from generator.recipe import Recipe
except ImportError:
    from flowcraft.generator.recipe import Recipe


class Denim(Recipe):
    """
    DEN-IM: Dengue Virus Identification from Metagenomic and Targeted Sequencing
    Standalone version available at https://github.com/assemblerflow/DEN-IM
    """

    def __init__(self):

        self.name = "denim"

        self.pipeline_str = "integrity_coverage " \
                            "fastqc_trimmomatic " \
                            "filter_poly " \
                            "bowtie " \
                            "retrieve_mapped " \
                            "check_coverage " \
                            "viral_assembly " \
                            "assembly_mapping " \
                            "pilon " \
                            "split_assembly " \
                            "dengue_typing " \
                            "mafft " \
                            "raxml"

        # Recipe parameters and directives
        self.directives = {
            "integrity_coverage": {
                "params": {"genomeSize": "0.012", "minCoverage": "10"}
            },
            "check_coverage": {
                "params": {"genomeSize": "0.012", "minCoverage": "10"}
            },
            "bowtie": {
                "params": {
                    "reference": "\"ref/DENV_MAPPING_V2.fasta\""}
            },
            "assembly_mapping": {
                "params": {"AMaxContigs": "1000", "genomeSize": "0.01"}
            },
            "split_assembly": {
                "params": {"splitSize": "10000"}
            }
        }