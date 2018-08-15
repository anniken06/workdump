#SingleInstance force

:*:;=::=================================================================================================================
:*:;pycode::import code; code.interact(local={{}**locals(), **globals(){}})
:*:;mci::mvn clean install
:*:;smci::mvn clean install -DskipTests
:*:;gcd::cd ~/git/coleman.ui/
:*:;gf::git fetch --all
:*:;gs::git stash
:*:;grh::git reset --hard
:*:;gru::git reset --hard @{{}u{}}
:*:;gcb::git checkout 
:*:;gt::git tag ""{Left}
:*:;gad::git add 
:*:;gcom::git commit -m ""{LEFT}
:*:;gpl::git pull 
:*:;gph::git push 
:*:;glog::git log --oneline 

:*:;sp::
{
	Send, System.out.println();
	Send, {Left}
	Send, {Left}
	Return
}

:*:;cls::
{
	Send, clear
	Send, {Enter}
	Sleep, 1000
	Click, 0, 0, right 
	Send, {DOWN 14}
	Send, {Enter}
	Return
}

:*:;rungit::
{
	Run "C:\Program Files\Git\git-bash.exe"
	Return
}

^SPACE:: Winset, Alwaysontop, , A
^UP:: WinSet, Style, +0xC00000, A
^DOWN:: WinSet, Style, -0xC00000, A
^RIGHT:: WinHide, A
^LEFT:: WinShow, A
