## ----------------------------------------
## Extra commands for the workflows workshop

## clean-sample-code: clean up outputs from the sample code
clean-sample-code :
	@echo Cleaning sample code ...
	@rm -rf code/snakemake/.snakemake/
	@rm -rf code/snakemake/results/
	@rm -rf code/nextflow/.nextflow/
	@rm -f code/nextflow/.nextflow.log*
	@rm -rf code/nextflow/results/
	@rm -rf code/nextflow/work/
	@rm -f code/Pipfile.lock
	@find code/ -name '*.pyc' -exec rm {} \;
	@rm -rf code/__pycache__/

## package-sample-code: package the sample code into downloadable archive
package-sample-code : clean-sample-code
	@echo Packing sample code ...
	@cd code && zip -r ../files/workflow-engines-lesson.zip *
	@cd code && tar czf ../files/workflow-engines-lesson.tar.gz *
