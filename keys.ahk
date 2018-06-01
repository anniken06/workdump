#SingleInstance force

::,=::=================================================================================================================
::,jpgit::https://github.com/johnpaulguzman/
::,mci::mvn clean install
::,smci::mvn clean install -DskipTests
::,cl::https://phmanjguzman01.infor.com:18000/coleman/{Enter}
::,cr::https://coleman2.awsiondev.infor.com:18010/coleman/{Enter}

:*:;ts::
{
	Send, .toString()
	Send, {Enter}
	Return
}

:*:;s::
{
	Send, System.out.println();
	Send, {Left}
	Send, {Left}
	Return
}

:*:;l::
{
	Send, lawson
	Send, {Tab}
	Send, lawson
	Send, {Enter}
	Return
}

:*:;t::
{
	Send, {Tab}
	Send, lbiadmin
	Send, {Tab}
	Send, LBITeam2010
	Send, {Enter}
	Return
}

:*:;j::
{
	Send, {Tab}
	Send, jguzman2
	Send, {Tab}
	Send, zxasqwQW{!}2
	Send, {Enter}
	Return
}


:*:;f::
{
	Send, {Tab}
	Send, fnarzoles
	Send, {Tab}
	Send, Wiyb{?}091183
	Send, {Enter}
	Return
}


^SPACE:: Winset, Alwaysontop, , A
^UP:: WinSet, Style, +0xC00000, A
^DOWN:: WinSet, Style, -0xC00000, A
