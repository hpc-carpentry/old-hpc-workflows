## ----------------------------------------
## Extra commands for the workflows workshop

## clean-sample-code: clean up outputs from the sample code
clean-sample-code :
	@echo Cleaning sample code ...
	@rm -rf code/.snakemake/ code/dats/ code/plots/ code/Pipfile.lock code/__pycache__/
	@find code/ -name '*.pyc' -exec rm {} \;

## package-sample-code: package the sample code into downloadable archive
package-sample-code : clean-sample-code
	@echo Packing sample code ...
	@cd code && zip -r ../files/workflow-engines-lesson.zip *
	@cd code && tar czf ../files/workflow-engines-lesson.tar.gz *
