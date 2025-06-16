ipconfig /flushdns
netsh winsock reset
Set-DnsClientServerAddress -InterfaceAlias "Wi-Fi" -ServerAddresses ("8.8.8.8", "8.8.4.4")
