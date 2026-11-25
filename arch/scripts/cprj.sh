exec_cprj() {
	local directory="${HOME}/Documents/Projects"
	if [[ -d $directory ]]; then
		local dir_children=$(find "${directory}" -mindepth 1 -maxdepth 1 -type d)
		local dir_children_count=$(find "${directory}" -mindepth 1 -maxdepth 1 -type d | wc -l)
		if [[ $dir_children_count -gt 0 ]]; then
			local response
			if [[ $dir_children_count -eq 1 ]]; then
				local sel_first_dir_children="$(find "${directory}" -mindepth 1 -maxdepth 1 -type d | awk "NR==1" | sed "s/ \// /g")"
				local target_dir="$(basename ${sel_first_dir_children})"
				local prompt_blue=$'\e[34m'
				local prompt_reset=$'\e[0m'
				echo "Projects directory contains one subdirectory."
				read -p "Move to ${prompt_blue}${target_dir}${prompt_reset}? [Y/n]: " response
				while true; do
					if [[ $response == "Y" || $response == "y" || $response == "" ]]; then
						cd "${sel_first_dir_children}"
						break
					elif [[ $response == "N" || $response == "n" ]]; then
						cd "${directory}"
						break
					else
						read -p "Type a valid option [Y/n]: " response
					fi
				done
			else
				local print_dir_children=""
				local prompt_blue=$'\e[34m'
				local prompt_reset=$'\e[0m'
				check_dir_children() {
					local iterator=1
					while (( iterator < dir_children_count + 1 )); do
						local target_dir="$(basename "$(find "${directory}" -mindepth 1 -maxdepth 1 -type d | awk "NR==${iterator}")")"
						print_dir_children+="[${iterator}] ${prompt_blue}${target_dir}${prompt_reset} "
						((iterator++))
					done
				}
				check_dir_children
				unset check_dir_children
				echo "Projects directory contains the following subdirectories:"
				echo $print_dir_children
				local response
				read -p $'Move to a subdirectory? [\e[3mnum\e[23m/N]: ' response
				while true; do
					if (( response > 0 && response < dir_children_count + 1 )); then
						local sel_dir_children="$(find "${directory}" -mindepth 1 -maxdepth 1 -type d | awk "NR==${response}" | sed "s/ \// /g")"
						cd "${sel_dir_children}"
						break
					elif [[ $response == "N" || $response == "n" || $response == "" ]]; then
						cd "${directory}"
						break
					else
						read -p $'Type a valid option [\e[3mnum\e[23m/N]: ' response
					fi
				done
			fi
		else
			cd "${directory}"
		fi
	else
		cd "${directory}"
	fi
}

exec_cprj
unset exec_cprj
