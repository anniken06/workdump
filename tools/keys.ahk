#SingleInstance force
CoordMode, Mouse, Screen;

; https://www.autohotkey.com/docs/KeyList.htm

:*:;pycode::import code; code.interact(local={{}**locals(), **globals(){}})
:*:;mci::mvn clean install
:*:;mcsi::mvn clean install -DskipTests
:*:;gcd::cd ~/git/coleman.ui/
:*:;grb::git rebase -i HEAD~
:*:;gfa::git fetch --all
:*:;grh::git reset --hard
:*:;gcb::git checkout
:*:;gtag::git tag ""{LEFT}
:*:;gadd::git add{SPACE}
:*:;gcom::git commit -m ""{LEFT}
:*:;gpl::git pull 
:*:;gph::git push 
:*:;glog::git log --oneline
:*:;gpr::git pull origin master --rebase
:*:;gst::git status

:*:;xp::xargs -I{{}{}}
:*:;tlh::tail -f -n {+}0 $(ls -t | head -1)
:*:;clh::cat $(ls -t | head -1)

:*:;jprint::
{
	Send, System.out.println();
	Send, {Left}
	Send, {Left}
	Return
}

:*:;rg::
{
	Run "C:\Program Files\Git\git-bash.exe"
	Return
}

; ^SPACE:: Winset, Alwaysontop, , A
; ^UP:: WinSet, Style, +0xC00000, A
; ^DOWN:: WinSet, Style, -0xC00000, A
; ^RIGHT:: WinHide, A
; ^LEFT:: WinShow, A
