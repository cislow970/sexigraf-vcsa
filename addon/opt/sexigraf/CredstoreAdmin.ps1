#!/usr/bin/pwsh -Command
# modified by Danilo Cilento <danilo.cilento@gmail.com>
#
param([Parameter (Mandatory=$true)] [string] $credstore, [string] $server, [string] $username, [string] $password, [string] $snmpv2comm, [string] $snmpv3user, [string] $snmpv3auth, [string] $snmpv3priv, [string] $active, [string] $passive, [string] $witness, [switch] $add, [switch] $remove, [switch] $list, [switch] $createstore, [switch] $check)

# https://www.powershellmagazine.com/2013/08/19/mastering-everyday-xml-tasks-in-powershell/
# https://github.com/dotnet/platform-compat/blob/master/docs/DE0001.md

try {
    if ($createstore -ne $true) {
        $createstorexml = New-Object -TypeName XML
        $createstorexml.Load($credstore)
    }
} catch {
    write-host "credstore not found or not valid xml"
    exit 1
}

if ($createstore) {
    if (!$(Test-Path $credstore)) {
        try {
            $XmlWriter = New-Object System.XMl.XmlTextWriter($credstore,$Null)
            $xmlWriter.Formatting = 'Indented'
            $xmlWriter.Indentation = 1
            $XmlWriter.IndentChar = "`t"
            $xmlWriter.WriteStartDocument()
            $xmlWriter.WriteProcessingInstruction("xml-stylesheet", "type='text/xsl' href='style.xsl'")
            $xmlWriter.WriteStartElement('viCredentials')
            $xmlWriter.WriteStartElement('passwordEntry')
            $xmlWriter.WriteElementString('server',"__localhost__")
            $xmlWriter.WriteElementString('username',"login")
            $xmlWriter.WriteElementString('password',"xxxxx")
            $xmlWriter.WriteElementString('snmpv2comm',"public")
            $xmlWriter.WriteElementString('snmpv3user',"monitor")
            $xmlWriter.WriteElementString('snmpv3auth',"xxxxx")
            $xmlWriter.WriteElementString('snmpv3priv',"xxxxx")
            $xmlWriter.WriteElementString('active',"10.10.10.1")
            $xmlWriter.WriteElementString('passive',"10.10.10.2")
            $xmlWriter.WriteElementString('witness',"10.10.10.3")
            $xmlWriter.WriteEndElement()  
            $xmlWriter.WriteEndDocument()
            $xmlWriter.Flush()
            $xmlWriter.Close()
        } catch {
            write-host "cannot create file"
            exit 1 
        }
    } else {
        write-host "file already exists"
        exit 1     
    }
} elseif ($check) {
    if ($server) {
        $XPath = '//passwordEntry[server="' + $server + '"]'
        if ($(Select-XML -Xml $createstorexml -XPath $XPath)){
            $item = Select-XML -Xml $createstorexml -XPath $XPath
            return $item.Node.count
        } else {
            return 0
        }
    } else {
        write-host "specify -server"
        exit 1
    }
} elseif ($list) {
    $viCredentialsList = @()
    foreach ($viCredential in $createstorexml.viCredentials.passwordEntry) {
        if ($viCredential.server.ToString() -ne "__localhost__") {
            $viCredentialEntry = "" | Select-Object server, username, snmpv2comm, snmpv3user, snmpv3auth, snmpv3priv, active, passive, witness
            $viCredentialEntry.server = $viCredential.server.ToString()
            $viCredentialEntry.username = $viCredential.username.ToString()
            $viCredentialEntry.snmpv2comm = $viCredential.snmpv2comm.ToString()
            $viCredentialEntry.snmpv3user = $viCredential.snmpv3user.ToString()
            $viCredentialEntry.snmpv3auth = [System.Text.Encoding]::Unicode.GetString([System.Convert]::FromBase64String($viCredential.snmpv3auth.ToString()))
            $viCredentialEntry.snmpv3priv = [System.Text.Encoding]::Unicode.GetString([System.Convert]::FromBase64String($viCredential.snmpv3priv.ToString()))
            $viCredentialEntry.active = $viCredential.active.ToString()
            $viCredentialEntry.passive = $viCredential.passive.ToString()
            $viCredentialEntry.witness = $viCredential.witness.ToString()
            $viCredentialsList += $viCredentialEntry
        }
    }
    $result = ""
    foreach ($elem in $viCredentialsList) {
        $result += $elem.server + "###" + $elem.username + "###" + $elem.snmpv2comm + "###" + $elem.snmpv3user + "###" + $elem.snmpv3auth + "###" + $elem.snmpv3priv + "###" + $elem.active + "###" + $elem.passive + "###" + $elem.witness
    }
    return $result
} elseif ($add) {
    if ($server -and $username -and $password) {
        $XPath = '//passwordEntry[server="' + $server + '"]'
        if (!$(Select-XML -Xml $createstorexml -XPath $XPath)){
            try {
                $item = Select-XML -Xml $createstorexml -XPath '//passwordEntry[1]'
                $newnode = $item.Node.CloneNode($true)
                $newnode.server = $server
                $newnode.username = $username
                $newnode.password = [Convert]::ToBase64String($([System.Text.Encoding]::Unicode.GetBytes($password)))
                $newnode.snmpv2comm = $snmpv2comm
                $newnode.snmpv3user = $snmpv3user
                $newnode.snmpv3auth = [Convert]::ToBase64String($([System.Text.Encoding]::Unicode.GetBytes($snmpv3auth)))
                $newnode.snmpv3priv = [Convert]::ToBase64String($([System.Text.Encoding]::Unicode.GetBytes($snmpv3priv)))
                $newnode.active = $active
                $newnode.passive = $passive
                $newnode.witness = $witness
                # [System.Text.Encoding]::Unicode.GetString([System.Convert]::FromBase64String($newnode.password))
                $passwordEntry = Select-XML -Xml $createstorexml -XPath '//viCredentials'
                $passwordEntry.Node.AppendChild($newnode)
                $createstorexml.Save($credstore)
            } catch {
                write-host "cannot add entry"
                exit 1 
            }
        } else {
            write-host "$server entry already exists"
            exit 1
        }
    } else {
        write-host "specify -server and -username and -password"
        exit 1
    }
} elseif ($remove) {
    if ($server) {
        try {
            $XPath = '//passwordEntry[server="' + $server + '"]'
            $item = Select-XML -Xml $createstorexml -XPath $XPath
            $null = $item.Node.ParentNode.RemoveChild($item.node)
            $createstorexml.Save($credstore)
        } catch {
            write-host "cannot remove entry"
            exit 1 
        }
    } else {
        write-host "specify -server"
        exit 1
    }
} else {
    write-host "specify -list, -createstore, -add, -remove or -check"
    exit 1
}
