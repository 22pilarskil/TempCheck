current_dir=$(pwd)

if [ ! -f "$current_dir/frozen_inference_graph.pb" ] ; then 
	echo "\033[0;96m~/Downloading frozen_inference_graph.pb\033[0m"
	wget -O "$current_dir/frozen_inference_graph.pb" \
		"https://www.dropbox.com/s/x617bfgof29rqya/frozen_inference_graph.pb?dl=1" \
		|| echo "\033[0;31~/Error downloading frozen_inference_graph.pb\033[0m"
fi