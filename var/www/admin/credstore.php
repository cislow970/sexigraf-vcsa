<?php
// modified by Danilo Cilento <danilo.cilento@gmail.com>
session_start();
//ini_set('display_errors', 'On');
$title = "SexiGraf vSphere Credential Store";
require("header.php");
require("helper.php");
?>
        <div class="container"><br/>
                <div class="panel panel-default">
                        <div class="panel-heading"><h3 class="panel-title">Credential Store Notes</h3></div>
                        <div class="panel-body"><ul>
                                <li>The credential store is used to store credentials and other parameters that will be used for vCenter/ESX query, it use vSphere SDK Credential Store Library.</li>
                                <li><font style="color:red;"><i class="glyphicon glyphicon-alert"></i></font> Removing a vCenter/ESX from the credential store will <b><font style="color:red;">NOT delete any collected metrics</font></b>.</li>
                                <li><b><font style="color:orange;">VCSA monitoring:</font></b> SNMPv2 monitoring must be enabled and therefore the community string must be entered. Alternatively, SNMPv3 can be used, in this case, the user, password auth and password priv must be entered. <b><font style="color:red;">SNMPv2 and SNMPv3 cannot be used together</font></b>.</li>
                                <li><b><font style="color:orange;">VCSA monitoring:</font></b> If vCenter clustering is not configured (VCHA) then leave HA active, passive and witness IP addresses blank.</li>
                                <li><b><font style="color:red;">If you enter the credentials for an ESX, unlike the vCenter, you must leave all fields related to SNMPv2/3 and the IP addresses for HA blank.</font></b></li>
                                <li>Please refer to the <a href="http://www.sexigraf.fr/">project website</a> and documentation for more information.</li>
                        </ul></div>
                </div>
                <h2><span class="glyphicon glyphicon-briefcase" aria-hidden="true"></span> SexiGraf Credential Store</h2>
                <table class="table table-hover">
                <thead><tr>
                        <th class="col-sm-4">vCenter/ESX address</th>
                        <th class="col-sm-3">Username</th>
                        <th class="col-sm-2">Password</th>
                        <th class="col-sm-2">SNMPv2 Community</th>
                        <th class="col-sm-2">SNMPv3 User</th>
                        <th class="col-sm-2">SNMPv3 Auth</th>
                        <th class="col-sm-2">SNMPv3 Priv</th>
                        <th class="col-sm-2">IP HA Active</th>
                        <th class="col-sm-2">IP HA Passive</th>
                        <th class="col-sm-2">IP HA Witness</th>
                        <th class="col-sm-1">VI</th>
                        <th class="col-sm-1">vSAN</th>
                        <th class="col-sm-1">VCSA</th>
                        <th class="col-sm-1">&nbsp;</th>
                </tr></thead>
        <tbody>
<?php
        // $credstoreData = shell_exec("/usr/lib/vmware-vcli/apps/general/credstore_admin.pl --credstore /var/www/.vmware/credstore/vicredentials.xml list");
        $credstoreData = shell_exec("/usr/bin/pwsh -NonInteractive -NoProfile -f /opt/sexigraf/CredstoreAdmin.ps1 -credstore /mnt/wfs/inventory/vipscredentials.xml -list");
        foreach(preg_split("/((\r?\n)|(\r\n?))/", $credstoreData) as $line) {
                if (strlen($line) == 0) { continue; }
                // if (preg_match('/^(?:(?!Server).)/', $line)) {
                if (preg_match('/^(?:(?!__localhost__).)/', $line)) {
                        $lineObjects = preg_split('/###/', $line);
                        echo '<tr><td>' . $lineObjects[0] . '</td><td>' . $lineObjects[1] . '</td><td>****</td><td>' . $lineObjects[2] . '</td><td>' . $lineObjects[3] . '</td><td>****</td><td>****</td><td>' . $lineObjects[6] . '</td><td>' . $lineObjects[7] . '</td><td>' . $lineObjects[8] . '</td>';
                        if (isViEnabled($lineObjects[0])) {
                                echo '                        <td><span class="glyphicon glyphicon-ok-sign" style="color:#5cb85c;font-size:2em;" aria-hidden="true"></span></td>';
                        } else {
                                echo '                        <td><span class="glyphicon glyphicon-remove-sign" style="color:#d9534f;font-size:2em;" aria-hidden="true"></span></td>';
                        }
                        if (isVsanEnabled($lineObjects[0])) {
                                echo '                        <td><span class="glyphicon glyphicon-ok-sign" style="color:#5cb85c;font-size:2em;" aria-hidden="true"></span></td>';
                        } else {
                                echo '                        <td><span class="glyphicon glyphicon-remove-sign" style="color:#d9534f;font-size:2em;" aria-hidden="true"></span></td>';
                        }
                        if (isVcsaEnabled($lineObjects[0])) {
                                echo '                        <td><span class="glyphicon glyphicon-ok-sign" style="color:#5cb85c;font-size:2em;" aria-hidden="true"></span></td>';
                        } else {
                                echo '                        <td><span class="glyphicon glyphicon-remove-sign" style="color:#d9534f;font-size:2em;" aria-hidden="true"></span></td>';
                        }
                        echo '                  <td><form class="form" action="credstore.php" method="post">
                                <input type="hidden" name="input-vcenter" value="' . $lineObjects[0] . '">
                                <input type="hidden" name="input-username" value="' . $lineObjects[1] . '">
                                <input type="hidden" name="input-snmpv2-comm" value="' . $lineObjects[2] . '">
                                <input type="hidden" name="input-snmpv3-user" value="' . $lineObjects[3] . '">
                                <input type="hidden" name="input-snmpv3-auth" value="' . $lineObjects[4] . '">
                                <input type="hidden" name="input-snmpv3-priv" value="' . $lineObjects[5] . '">
                                <input type="hidden" name="input-haip-active" value="' . $lineObjects[6] . '">
                                <input type="hidden" name="input-haip-passive" value="' . $lineObjects[7] . '">
                                <input type="hidden" name="input-haip-witness" value="' . $lineObjects[8] . '">
                                <div class="btn-group">
                                        <button type="button" class="btn btn-primary dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                                Action <span class="caret"></span>
                                        </button>
                                        <ul class="dropdown-menu">';
                        if (isViEnabled($lineObjects[0])) {
                                echo '                          <li><button name="submit" class="btn btn-link btn-xs" value="disable-vi">Disable VI</button></li>';
                        } else {
                                echo '                          <li><button name="submit" class="btn btn-link btn-xs" value="enable-vi">Enable VI</button></li>';
                        }
                        if (isVsanEnabled($lineObjects[0])) {
                                echo '                          <li><button name="submit" class="btn btn-link btn-xs" value="disable-vsan">Disable vSAN</button></li>';
                        } else {
                                echo '                          <li><button name="submit" class="btn btn-link btn-xs" value="enable-vsan">Enable vSAN</button></li>';
                        }
                        if (isVcsaEnabled($lineObjects[0])) {
                                echo '                          <li><button name="submit" class="btn btn-link btn-xs" value="disable-vcsa">Disable VCSA</button></li>';
                        } else {
                                echo '                          <li><button name="submit" class="btn btn-link btn-xs" value="enable-vcsa">Enable VCSA</button></li>';
                        }
                        echo '                          <li role="separator" class="divider"></li>
                                <li><button name="submit" class="btn btn-link btn-xs" value="delete-vcentry">Delete</button></li>
                                        </ul>
                                </div>
                        </form></td>
                </tr>
';
                }
        }
?>
                <tr><form class="form" action="credstore.php" method="post">
                        <td><input type="text" class="form-control" name="input-vcenter" placeholder="vCenter IP or FQDN" aria-describedby="vcenter-label"></td>
                        <td><input type="text" class="form-control" name="input-username" placeholder="Username" aria-describedby="username-label"></td>
                        <td><input type="password" class="form-control" name="input-password" placeholder="Password" aria-describedby="password-label"></td>
                        <td><input type="text" class="form-control" name="input-snmpv2-comm" placeholder="SNMPv2 Community" aria-describedby="snmpcomm-label"></td>
                        <td><input type="text" class="form-control" name="input-snmpv3-user" placeholder="SNMPv3 Username" aria-describedby="snmpuser-label"></td>
                        <td><input type="password" class="form-control" name="input-snmpv3-auth" placeholder="SNMPv3 Auth Password" aria-describedby="snmpauth-label"></td>
                        <td><input type="password" class="form-control" name="input-snmpv3-priv" placeholder="SNMPv3 Priv Password" aria-describedby="snmppriv-label"></td>
                        <td><input type="text" class="form-control" name="input-haip-active" placeholder="IP HA Active" aria-describedby="active-label"></td>
                        <td><input type="text" class="form-control" name="input-haip-passive" placeholder="IP HA Passive" aria-describedby="passive-label"></td>
                        <td><input type="text" class="form-control" name="input-haip-witness" placeholder="IP HA Witness" aria-describedby="witness-label"></td>
                        <td>&nbsp;*</td>
                        <td>&nbsp;*</td>
                        <td>&nbsp;*</td>
                        <td><button name="submit" class="btn btn-success" value="addmodify" onclick="document.getElementById('submitmessage').style.display = 'block'">Add</button></td>
                </form></tr>
                </tbody>
                </table>
                <div id="submitmessage" class="alert alert-warning" role="warning" style="display: none">
                <span class="glyphicon glyphicon-exclamation-sign" aria-hidden="true"></span>
                <span class="sr-only">Warning:</span>Please wait while we validate server reachability and user access...
                </div>
<?php
        if ($_SERVER['REQUEST_METHOD'] == 'POST') {
                switch ($_POST["submit"]) {
                        case "addmodify":
                                $errorHappened = false;

                                if (empty($_POST["input-snmpv2-comm"])) {
                                        $snmpv2_comm = "none";
                                } else {
                                        $snmpv2_comm = $_POST["input-snmpv2-comm"];
                                }
                                if (empty($_POST["input-snmpv3-user"])) {
                                        $snmpv3_user = "none";
                                } else {
                                        $snmpv3_user = $_POST["input-snmpv3-user"];
                                }
                                if (empty($_POST["input-snmpv3-auth"])) {
                                        $snmpv3_auth = "none";
                                } else {
                                        $snmpv3_auth = $_POST["input-snmpv3-auth"];
                                }
                                if (empty($_POST["input-snmpv3-priv"])) {
                                        $snmpv3_priv = "none";
                                } else {
                                        $snmpv3_priv = $_POST["input-snmpv3-priv"];
                                }
                                if (empty($_POST["input-haip-active"])) {
                                        $haip_active = "none";
                                } else {
                                        $haip_active = $_POST["input-haip-active"];
                                }
                                if (empty($_POST["input-haip-passive"])) {
                                        $haip_passive = "none";
                                } else {
                                        $haip_passive = $_POST["input-haip-passive"];
                                }
                                if (empty($_POST["input-haip-witness"])) {
                                        $haip_witness = "none";
                                } else {
                                        $haip_witness = $_POST["input-haip-witness"];
                                }

                                if (empty($_POST["input-vcenter"]) or empty($_POST["input-username"]) or empty($_POST["input-password"])) {
                                        $errorHappened = true;
                                        $errorMessage = "All mandatory values have not been provided.";
                                } elseif (!filter_var($_POST["input-vcenter"], FILTER_VALIDATE_IP) and (gethostbyname($_POST["input-vcenter"]) == $_POST["input-vcenter"])) {
                                        $errorHappened = true;
                                        $errorMessage = "vCenter/ESX IP or FQDN is not correct.";
                                } elseif (shell_exec("/usr/bin/pwsh -NonInteractive -NoProfile -f /opt/sexigraf/CredstoreAdmin.ps1 -credstore /mnt/wfs/inventory/vipscredentials.xml -check -server " . $_POST["input-vcenter"]) > 0) {
                                        $errorHappened = true;
                                        $errorMessage = "vCenter/ESX IP or FQDN is already in credential store, duplicate entry is not supported.";
                                } elseif (preg_match("/^([a-zA-Z0-9-_.]*)\\\\?([a-zA-Z0-9-_.]+)$|^([a-zA-Z0-9-_.]*)$|^([a-zA-Z0-9-_.]+)@([a-zA-Z0-9-_.]*)$/", $_POST["input-username"]) == 0) {
                                        $errorHappened = true;
                                        $errorMessage = "Wrong username format, supported format are DOMAIN\USERNAME, USERNAME, USERNAME@DOMAIN.TLD";
                                } elseif (($snmpv2_comm != "none") and ($snmpv3_user != "none")) {
                                        $errorHappened = true;
                                        $errorMessage = "SNMPv2 and SNMPv3 cannot be used together. If you enter the credentials for an ESX, you must leave all fields related to SNMPv2/3 and the IP addresses for HA blank.";
                                } elseif (($snmpv3_user != "none") and (($snmpv3_auth == "none") or ($snmpv3_priv == "none"))) {
                                        $errorHappened = true;
                                        $errorMessage = "If SNMPv3 user is configured then its authentication password and privacy password must also be configured.";
                                } else {
                                        # if input seems to be well-formated, we just need to test a connection query
                                        // exec("/usr/lib/vmware-vcli/apps/general/connect.pl --server " . escapeshellcmd($_POST["input-vcenter"]) . " --username " . escapeshellcmd($_POST["input-username"]) . " --password " . escapeshellcmd($_POST["input-password"]), $null, $return_var);
                                        exec("/usr/bin/pwsh -NonInteractive -NoProfile -f /opt/sexigraf/ViConnect.ps1 -server " . escapeshellcmd($_POST["input-vcenter"]) . " -username " . escapeshellcmd($_POST["input-username"]) . " -password " . escapeshellcmd($_POST["input-password"]), $null, $return_var);
                                        if ($return_var) {
                                                $errorHappened = true;
                                                $errorMessage = "Wrong username/password or no answer at TCP:443";
                                        }
                                }

                                if ($errorHappened) {
                                        echo '  <div class="alert alert-danger" role="alert">
                                        <span class="glyphicon glyphicon-exclamation-sign" aria-hidden="true"></span>
                                        <span class="sr-only">Error:</span>
                                        ' . $errorMessage . '
                                        </div>';
                                        echo '<script type="text/javascript">setTimeout(function(){ location.replace("credstore.php"); }, 2000);</script>';
                                } else {
                                        echo '  <div class="alert alert-success" role="alert">
                                        <span class="glyphicon glyphicon-ok" aria-hidden="true"></span>
                                        <span class="sr-only">Success:</span> Success!';
                                        // echo shell_exec("/usr/lib/vmware-vcli/apps/general/credstore_admin.pl --credstore /var/www/.vmware/credstore/vicredentials.xml add --server " . $_POST["input-vcenter"] . " --username " . escapeshellcmd($_POST["input-username"]) . " --password " . escapeshellcmd($_POST["input-password"]));
                                        echo exec("/usr/bin/pwsh -NonInteractive -NoProfile -f /opt/sexigraf/CredstoreAdmin.ps1 -credstore /mnt/wfs/inventory/vipscredentials.xml -add -server " . escapeshellcmd($_POST["input-vcenter"]) . " -username " . escapeshellcmd($_POST["input-username"]) . " -password " . escapeshellcmd($_POST["input-password"]) . " -snmpv2comm " . escapeshellcmd($snmpv2_comm) . " -snmpv3user " . escapeshellcmd($snmpv3_user) . " -snmpv3auth " . escapeshellcmd($snmpv3_auth) . " -snmpv3priv " . escapeshellcmd($snmpv3_priv) . " -active " . escapeshellcmd($haip_active) . " -passive " . escapeshellcmd($haip_passive) . " -witness " . escapeshellcmd($haip_witness));
                                        // Once newly vCenter has been added, we want the inventory to be updated
                                        shell_exec("sudo /bin/bash /var/www/scripts/updateInventory.sh > /dev/null 2>/dev/null &");
                                        echo '  </div>';
                                        echo '<script type="text/javascript">setTimeout(function(){ location.replace("credstore.php"); }, 2000);</script>';
                                }
                                break;
                        case "delete-vcentry":
                                echo '  <div class="alert alert-warning" role="warning">
                <h4><span class="glyphicon glyphicon-alert" aria-hidden="true"></span>
                <span class="sr-only">Warning:</span>
                Confirmation needed!</h4>
                You are about to delete entry from VMware Credential Store for ' . $_POST["input-vcenter"] . '. Are you sure about this? We mean, <strong>really sure</strong>?<br />
                <form class="form" action="credstore.php" method="post">
                        <input type="hidden" name="input-vcenter" value="' . $_POST["input-vcenter"] . '">
                        <input type="hidden" name="input-username" value="' . $_POST["input-username"] . '">
                        <p><button name="submit" class="btn btn-warning" value="delete-vcentry-confirmed">Delete entry</button></p>
                </form>';
                                echo '  </div>';
                                break;
                        case "delete-vcentry-confirmed":
                                disableVi($_POST["input-vcenter"]);
                                disableVsan($_POST["input-vcenter"]);
                                disableVcsa($_POST["input-vcenter"]);
                                echo '  <div class="alert alert-success" role="alert">
                <span class="glyphicon glyphicon-ok" aria-hidden="true"></span>
                <span class="sr-only">Success:</span>';
                                // shell_exec("/usr/lib/vmware-vcli/apps/general/credstore_admin.pl --credstore /var/www/.vmware/credstore/vicredentials.xml remove --server " . $_POST["input-vcenter"] . " --username " . escapeshellcmd($_POST["input-username"]));
                                echo exec("/usr/bin/pwsh -NonInteractive -NoProfile -f /opt/sexigraf/CredstoreAdmin.ps1 -credstore /mnt/wfs/inventory/vipscredentials.xml -remove -server " . escapeshellcmd($_POST["input-vcenter"])) . "Refreshing...";
                                shell_exec("sudo /bin/bash /var/www/scripts/updateInventory.sh > /dev/null 2>/dev/null &");
                                echo '  </div>';
                                echo '<script type="text/javascript">setTimeout(function(){ location.replace("credstore.php"); }, 1000);</script>';
                                break;
                        case "enable-vi":
                                enableVi($_POST["input-vcenter"]);
                                echo '  <div class="alert alert-success" role="alert">
                <span class="glyphicon glyphicon-ok" aria-hidden="true"></span>
                <span class="sr-only">Success:</span>
                VI query successfully enabled for ' . $_POST["input-vcenter"] . ', refreshing...
        </div>
        <script type="text/javascript">setTimeout(function(){ location.replace("credstore.php"); }, 1000);</script>';
                                break;
                        case "enable-vsan":
                                enableVsan($_POST["input-vcenter"]);
                                echo '  <div class="alert alert-success" role="alert">
                <span class="glyphicon glyphicon-ok" aria-hidden="true"></span>
                <span class="sr-only">Success:</span>
                vSAN query successfully enabled for ' . $_POST["input-vcenter"] . ', refreshing...
        </div>
        <script type="text/javascript">setTimeout(function(){ location.replace("credstore.php"); }, 1000);</script>';
                                break;
                        case "enable-vcsa":
                                enableVcsa($_POST["input-vcenter"], $_POST["input-snmpv2-comm"], $_POST["input-snmpv3-user"], $_POST["input-snmpv3-auth"], $_POST["input-snmpv3-priv"], $_POST["input-haip-active"], $_POST["input-haip-passive"], $_POST["input-haip-witness"]);
                                echo '  <div class="alert alert-success" role="alert">
                <span class="glyphicon glyphicon-ok" aria-hidden="true"></span>
                <span class="sr-only">Success:</span>
                VCSA query successfully enabled for ' . $_POST["input-vcenter"] . ', refreshing...
        </div>
        <script type="text/javascript">setTimeout(function(){ location.replace("credstore.php"); }, 1000);</script>';
                                break;
                        case "disable-vi":
                                disableVi($_POST["input-vcenter"]);
                                echo '  <div class="alert alert-success" role="alert">
                <span class="glyphicon glyphicon-ok" aria-hidden="true"></span>
                <span class="sr-only">Success:</span>
                VI query successfully disabled for ' . $_POST["input-vcenter"] . ', refreshing...
        </div>
        <script type="text/javascript">setTimeout(function(){ location.replace("credstore.php"); }, 1000);</script>';
                                break;
                        case "disable-vsan":
                                disableVsan($_POST["input-vcenter"]);
                                echo '  <div class="alert alert-success" role="alert">
                <span class="glyphicon glyphicon-ok" aria-hidden="true"></span>
                <span class="sr-only">Success:</span>
                vSAN query successfully disabled for ' . $_POST["input-vcenter"] . ', refreshing...
        </div>
        <script type="text/javascript">setTimeout(function(){ location.replace("credstore.php"); }, 1000);</script>';
                                break;
                        case "disable-vcsa":
                                disableVcsa($_POST["input-vcenter"]);
                                echo '  <div class="alert alert-success" role="alert">
                <span class="glyphicon glyphicon-ok" aria-hidden="true"></span>
                <span class="sr-only">Success:</span>
                VCSA query successfully disabled for ' . $_POST["input-vcenter"] . ', refreshing...
        </div>
        <script type="text/javascript">setTimeout(function(){ location.replace("credstore.php"); }, 1000);</script>';
                                break;
                }
        }
?>
        </div>
        <script type="text/javascript" src="js/bootstrap.min.js"></script>
</body>
</html>
