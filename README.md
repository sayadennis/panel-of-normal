# Evaluation of GATK Panel of Normals

## Background 

Many institutions have a large collection of preserved tissue samples of cancerous or benign origin. In order to study the genomic profiles of these samples, it is necessary to differentiate which genomic characteristics, such as DNA sequence variations and copy-number variations, are from germline (i.e. patient is born with these variations) or somatic (i.e. the variation accumulated after both). The Broad Institute's [GATK](https://gatk.broadinstitute.org/hc/en-us) has developed a tool called [Panel of Normals (PON)](https://gatk.broadinstitute.org/hc/en-us/articles/360035890631-Panel-of-Normals-PON-), in which we can generate a representative collection of "normal" samples to be used to characterize the somatic genomic aberrations. 

There are a number of publicly available PONs, generated from large-scale studies like 1000-genome project (`gs://gatk-best-practices/somatic-hg38/1000g_pon.hg38.vcf.gz` foundunder the [GATK Resource Bundle](https://gatk.broadinstitute.org/hc/en-us/articles/360035890811-Resource-bundle)). Although these PONs offer the advantage of a large sample size, creating an in-house PON might be beneficial in a sense that it better represents any germline variant patterns that is unique to the specific cohort of interest. 

Using GATK's [CreateSomaticPanelOfNormals](https://gatk.broadinstitute.org/hc/en-us/articles/360037058172-CreateSomaticPanelOfNormals-BETA-) function, we can input as many or as few normal samples as we have. However, there is no information as to how the accuracy of somatic variant calls is affected by the number of normal samples that go into the PON. 

## Project goal 

In this project, we aim to evaluate how the "wellness" of variant calls are affected by the number of samples that go into the PON. 

<!-- ## Approach 

## Results  -->
