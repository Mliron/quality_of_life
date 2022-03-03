global_dest_dir = /usr/local/bin
script_file = auto_run.py

help:
	@echo "Options:"
	@echo "  run         - runs the script (only with --help since this script needs something to track)"
	@echo "  globalize   - Creates a symbolic link inside '$(global_dest_dir)' directory"
	@echo "  deglobalize - Deletes the symbolic link from '$(global_dest_dir)'"

run: $(script_file)
	python3 $< --help

globalize: $(script_file)
	sudo ln -s $(PWD)/$(script_file) $(global_dest_dir)/$(script_file)

deglobalize: $(global_dest_dir)/$(script_file)
	sudo rm $<
