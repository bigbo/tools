# wiki 插件
## 1.Mrakdown插件使用:
  require_once("$IP/extensions/MarkdownExtraGeshiSyntax/MarkdownExtraGeshiSyntax.php");
## 2.passport插件使用:
  $wgGroupPermissions['*']['createaccount'] = false;
  require_once( "$IP/extensions/PassportAuth/PassportAuthPlugin.php");
  $wgAuth = new PassportAuthPlugin();
## 3.自定义分组插件使用:
  $wgExtraNamespaces = array(700 => "dev", 701 => "dev_Talk", 702 => "test", 703 => "test_Talk");
  require_once('extensions/NamespacePermissions.php');

